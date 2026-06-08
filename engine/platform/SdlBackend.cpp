#include "engine/platform/SdlBackend.hpp"

#include <SDL_mixer.h>

#include <algorithm>
#include <filesystem>
#include <iostream>
#include <stdexcept>

namespace novel::platform {

namespace {

/// Return byte-offset of each UTF-8 code point, plus a sentinel at end.
std::vector<std::size_t> utf8_char_offsets(const std::string& text) {
    std::vector<std::size_t> offsets;
    offsets.reserve(text.size() + 1);
    for (std::size_t i = 0; i < text.size(); ) {
        offsets.push_back(i);
        auto c = static_cast<unsigned char>(text[i]);
        if      (c < 0x80)            i += 1;
        else if ((c >> 5) == 0x06)    i += 2;
        else if ((c >> 4) == 0x0E)    i += 3;
        else if ((c >> 3) == 0x1E)    i += 4;
        else                          i += 1;
    }
    offsets.push_back(text.size());
    return offsets;
}

} // namespace

SdlBackend::SdlBackend(int width, int height, const std::string& title,
                         const std::string& content_root)
    : width_(width), height_(height), title_(title), content_root_(content_root) {}

SdlBackend::~SdlBackend() { shutdown(); }

// ─── Font loading / reloading (scaled to current resolution) ─────────────────

bool SdlBackend::reload_fonts() {
    if (font_title_ && font_title_ != font_) TTF_CloseFont(font_title_);
    if (font_small_ && font_small_ != font_) TTF_CloseFont(font_small_);
    if (font_) TTF_CloseFont(font_);
    font_ = font_small_ = font_title_ = nullptr;

    int base_size  = std::max(sy(24), 10);
    int small_size = std::max(sy(20), 8);
    int title_size = std::max(sy(48), 16);

    const std::string font_path = resolve_path("fonts/default.ttf");
    font_ = TTF_OpenFont(font_path.c_str(), base_size);
    if (!font_)
        font_ = TTF_OpenFont("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", base_size);
    if (!font_) {
        std::cerr << "TTF_OpenFont failed: " << TTF_GetError() << '\n';
        return false;
    }

    font_small_ = TTF_OpenFont(font_path.c_str(), small_size);
    if (!font_small_)
        font_small_ = TTF_OpenFont("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", small_size);
    if (!font_small_)
        font_small_ = font_;

    const std::string title_font_path = resolve_path("gui/font/RifficFree-Bold.ttf");
    font_title_ = TTF_OpenFont(title_font_path.c_str(), title_size);
    if (!font_title_)
        font_title_ = font_;

    return true;
}

bool SdlBackend::init() {
    if (SDL_Init(SDL_INIT_VIDEO | SDL_INIT_AUDIO) != 0) {
        std::cerr << "SDL_Init failed: " << SDL_GetError() << '\n';
        return false;
    }

    if (IMG_Init(IMG_INIT_PNG | IMG_INIT_JPG) == 0) {
        std::cerr << "IMG_Init failed: " << IMG_GetError() << '\n';
        return false;
    }

    if (TTF_Init() != 0) {
        std::cerr << "TTF_Init failed: " << TTF_GetError() << '\n';
        return false;
    }

    if (Mix_OpenAudio(44100, MIX_DEFAULT_FORMAT, 2, 2048) < 0) {
        std::cerr << "Mix_OpenAudio failed: " << Mix_GetError() << '\n';
        return false;
    }
    Mix_AllocateChannels(16);

    window_ = SDL_CreateWindow(title_.c_str(), SDL_WINDOWPOS_CENTERED,
                               SDL_WINDOWPOS_CENTERED, width_, height_,
                               SDL_WINDOW_SHOWN | SDL_WINDOW_ALLOW_HIGHDPI);
    if (!window_) {
        std::cerr << "SDL_CreateWindow failed: " << SDL_GetError() << '\n';
        return false;
    }

    renderer_ = SDL_CreateRenderer(window_, -1,
                                   SDL_RENDERER_ACCELERATED | SDL_RENDERER_PRESENTVSYNC);
    if (!renderer_) {
        std::cerr << "SDL_CreateRenderer failed: " << SDL_GetError() << '\n';
        return false;
    }

    if (!reload_fonts()) return false;

    running_ = true;
    return true;
}

void SdlBackend::shutdown() {
    if (shutdown_done_) return;
    shutdown_done_ = true;

    Mix_HaltChannel(-1);
    if (current_music_) {
        Mix_HaltMusic();
        current_music_.reset();
    }
    chunk_cache_.clear();
    Mix_CloseAudio();

    sprites_.clear();
    background_ = nullptr;
    texture_cache_.clear();

    if (font_title_ && font_title_ != font_) TTF_CloseFont(font_title_);
    if (font_small_ && font_small_ != font_) TTF_CloseFont(font_small_);
    if (font_) TTF_CloseFont(font_);
    font_ = nullptr;
    font_small_ = nullptr;
    font_title_ = nullptr;

    if (renderer_) SDL_DestroyRenderer(renderer_);
    if (window_) SDL_DestroyWindow(window_);
    renderer_ = nullptr;
    window_ = nullptr;

    TTF_Quit();
    IMG_Quit();
    SDL_Quit();
}

std::string SdlBackend::resolve_path(const std::string& relative) const {
    std::filesystem::path full = std::filesystem::path(content_root_) / relative;
    return full.string();
}

SDL_Texture* SdlBackend::load_texture(const std::string& path) {
    const auto it = texture_cache_.find(path);
    if (it != texture_cache_.end()) {
        return it->second.get();
    }

    const std::string full_path = resolve_path(path);
    SDL_Surface* surface = IMG_Load(full_path.c_str());
    if (!surface) {
        std::cerr << "Failed to load image: " << full_path << " (" << IMG_GetError() << ")\n";
        return nullptr;
    }

    SDL_Texture* texture = SDL_CreateTextureFromSurface(renderer_, surface);
    SDL_FreeSurface(surface);
    texture_cache_[path] = sdl_raii::TexturePtr(texture);
    return texture;
}

void SdlBackend::render_frame() {
    SDL_SetRenderDrawColor(renderer_, 0, 0, 0, 255);
    SDL_RenderClear(renderer_);
    render_background();
    render_sprites();
}

void SdlBackend::render_background() {
    if (!background_) return;
    SDL_RenderCopy(renderer_, background_, nullptr, nullptr);
}

void SdlBackend::render_sprites() {
    for (auto& [tag, sprite] : sprites_) {
        if (!sprite.texture) continue;

        int x = width_ / 2 - sprite.w / 2;
        if (sprite.position == "left") {
            x = width_ / 6 - sprite.w / 2;
        } else if (sprite.position == "right") {
            x = width_ * 5 / 6 - sprite.w / 2;
        }

        int y = height_ - sprite.h;

        SDL_Rect dst = {x, y, sprite.w, sprite.h};
        SDL_RenderCopy(renderer_, sprite.texture, nullptr, &dst);
    }
}

void SdlBackend::render_textbox(const std::string& speaker, const std::string& text) {
    const int box_height = sy(185);

    SDL_Texture* tb_tex = load_texture("gui/textbox.png");
    if (tb_tex) {
        int tw, th;
        SDL_QueryTexture(tb_tex, nullptr, nullptr, &tw, &th);
        float scale = static_cast<float>(width_) * 0.8f / static_cast<float>(tw);
        int draw_w = static_cast<int>(tw * scale);
        int draw_h = static_cast<int>(th * scale);
        SDL_Rect tb_dst = {(width_ - draw_w) / 2, height_ - draw_h - sy(10), draw_w, draw_h};
        SDL_RenderCopy(renderer_, tb_tex, nullptr, &tb_dst);
    } else {
        int box_y = height_ - box_height;
        SDL_SetRenderDrawBlendMode(renderer_, SDL_BLENDMODE_BLEND);
        SDL_SetRenderDrawColor(renderer_, 0, 0, 0, 200);
        SDL_Rect box = {0, box_y, width_, box_height};
        SDL_RenderFillRect(renderer_, &box);
        SDL_SetRenderDrawColor(renderer_, 200, 200, 200, 255);
        SDL_RenderDrawRect(renderer_, &box);
    }

    const int text_left = width_ / 8;
    int text_y = height_ - box_height + sy(30);

    if (!speaker.empty()) {
        SDL_Color name_color = {90, 40, 80, 255};
        SDL_Surface* name_surface = TTF_RenderUTF8_Blended(font_, speaker.c_str(), name_color);
        if (name_surface) {
            SDL_Texture* name_tex = SDL_CreateTextureFromSurface(renderer_, name_surface);
            SDL_Rect name_rect = {text_left, text_y, name_surface->w, name_surface->h};
            SDL_RenderCopy(renderer_, name_tex, nullptr, &name_rect);
            text_y += name_surface->h + sy(6);
            SDL_DestroyTexture(name_tex);
            SDL_FreeSurface(name_surface);
        }
    }

    SDL_Color text_color = {20, 20, 20, 255};
    text_wrap_render(text, text_left, text_y, width_ - text_left * 2, text_color);
}

SDL_Rect SdlBackend::text_wrap_render(const std::string& text, int x, int y, int max_width,
                                       SDL_Color color) {
    if (text.empty()) return {x, y, 0, 0};

    SDL_Surface* surface = TTF_RenderUTF8_Blended_Wrapped(font_small_, text.c_str(), color,
                                                           static_cast<Uint32>(max_width));
    if (!surface) return {x, y, 0, 0};

    SDL_Texture* tex = SDL_CreateTextureFromSurface(renderer_, surface);
    SDL_Rect dst = {x, y, surface->w, surface->h};
    SDL_RenderCopy(renderer_, tex, nullptr, &dst);
    SDL_DestroyTexture(tex);
    SDL_FreeSurface(surface);
    return dst;
}

void SdlBackend::render_choices(const std::vector<std::string>& options, int highlight) {
    SDL_Texture* idle_bg = load_texture("gui/button/choice_idle_background.png");
    SDL_Texture* hover_bg = load_texture("gui/button/choice_hover_background.png");

    ChoiceLayout layout(width_, height_, static_cast<int>(options.size()));

    for (int i = 0; i < static_cast<int>(options.size()); ++i) {
        int iy = layout.item_y(i);
        SDL_Rect dst = {layout.item_x, iy, layout.item_w, layout.item_h};

        SDL_Texture* bg = (i == highlight) ? hover_bg : idle_bg;
        if (bg) {
            SDL_RenderCopy(renderer_, bg, nullptr, &dst);
        } else {
            SDL_SetRenderDrawBlendMode(renderer_, SDL_BLENDMODE_BLEND);
            if (i == highlight) {
                SDL_SetRenderDrawColor(renderer_, 255, 182, 193, 200);
            } else {
                SDL_SetRenderDrawColor(renderer_, 40, 40, 60, 200);
            }
            SDL_RenderFillRect(renderer_, &dst);
            SDL_SetRenderDrawColor(renderer_, 200, 200, 200, 180);
            SDL_RenderDrawRect(renderer_, &dst);
        }

        SDL_Color color = (i == highlight) ? SDL_Color{60, 20, 40, 255}
                                           : SDL_Color{50, 30, 50, 255};
        const std::string label = options[static_cast<std::size_t>(i)];
        SDL_Surface* surface = TTF_RenderUTF8_Blended_Wrapped(
            font_, label.c_str(), color, static_cast<Uint32>(layout.item_w - sx(40)));
        if (surface) {
            SDL_Texture* tex = SDL_CreateTextureFromSurface(renderer_, surface);
            SDL_Rect text_dst = {layout.item_x + sx(20),
                                 iy + (layout.item_h - surface->h) / 2,
                                 surface->w, surface->h};
            SDL_RenderCopy(renderer_, tex, nullptr, &text_dst);
            SDL_DestroyTexture(tex);
            SDL_FreeSurface(surface);
        }
    }
}

FlowSignal SdlBackend::wait_for_advance() {
    SDL_RenderPresent(renderer_);

    while (running_) {
        SDL_Event event;
        while (SDL_PollEvent(&event)) {
            if (event.type == SDL_QUIT) {
                running_ = false;
                return FlowSignal::Quit;
            }
            if (event.type == SDL_KEYDOWN) {
                if (event.key.keysym.sym == SDLK_RETURN || event.key.keysym.sym == SDLK_SPACE) {
                    return FlowSignal::Continue;
                }
                if (event.key.keysym.sym == SDLK_ESCAPE) {
                    GameSettings settings;
                    settings.music_volume = music_volume_ * 100 / MIX_MAX_VOLUME;
                    settings.sfx_volume = sfx_volume_ * 100 / MIX_MAX_VOLUME;
                    PauseAction action = show_pause_menu();
                    if (action == PauseAction::Quit) {
                        return FlowSignal::Quit;
                    }
                    if (action == PauseAction::MainMenu) {
                        return FlowSignal::MainMenu;
                    }
                    if (action == PauseAction::Settings) {
                        show_settings(settings);
                        apply_settings(settings);
                    }
                    render_frame();
                    render_textbox("", "");
                    SDL_RenderPresent(renderer_);
                }
            }
            if (event.type == SDL_MOUSEBUTTONDOWN) {
                return FlowSignal::Continue;
            }
        }
        SDL_Delay(16);
    }
    return FlowSignal::Quit;
}

// ─── Typewriter effect ───────────────────────────────────────────────────────

FlowSignal SdlBackend::render_typewriter(const std::string& speaker, const std::string& text) {
    auto offsets = utf8_char_offsets(text);
    std::size_t total_chars = offsets.size() - 1;

    if (total_chars == 0) {
        render_frame();
        render_textbox(speaker, "");
        return wait_for_advance();
    }

    int delay_ms = 101 - text_speed_;
    if (delay_ms < 1) delay_ms = 1;
    Uint32 start_time = SDL_GetTicks();
    bool completed = false;

    while (running_ && !completed) {
        Uint32 elapsed = SDL_GetTicks() - start_time;
        std::size_t target = std::min(
            static_cast<std::size_t>(elapsed / static_cast<Uint32>(delay_ms)), total_chars);

        std::string partial = text.substr(0, offsets[target]);
        render_frame();
        render_textbox(speaker, partial);
        SDL_RenderPresent(renderer_);

        if (target >= total_chars) {
            completed = true;
            break;
        }

        SDL_Event event;
        while (SDL_PollEvent(&event)) {
            if (event.type == SDL_QUIT) {
                running_ = false;
                return FlowSignal::Quit;
            }
            if (event.type == SDL_KEYDOWN) {
                if (event.key.keysym.sym == SDLK_ESCAPE) {
                    GameSettings settings;
                    settings.music_volume = music_volume_ * 100 / MIX_MAX_VOLUME;
                    settings.sfx_volume = sfx_volume_ * 100 / MIX_MAX_VOLUME;
                    PauseAction action = show_pause_menu();
                    if (action == PauseAction::Quit) return FlowSignal::Quit;
                    if (action == PauseAction::MainMenu) return FlowSignal::MainMenu;
                    if (action == PauseAction::Settings) {
                        show_settings(settings);
                        apply_settings(settings);
                    }
                    completed = true;
                } else {
                    completed = true;
                }
            }
            if (event.type == SDL_MOUSEBUTTONDOWN) {
                completed = true;
            }
        }
        SDL_Delay(16);
    }

    render_frame();
    render_textbox(speaker, text);
    return wait_for_advance();
}

FlowSignal SdlBackend::say(const std::string& speaker, const std::string& text) {
    if (text_speed_ == 0) {
        render_frame();
        render_textbox(speaker, text);
        return wait_for_advance();
    }
    return render_typewriter(speaker, text);
}

// ─── Choice menu ─────────────────────────────────────────────────────────────

ChoiceResult SdlBackend::choose(const std::vector<std::string>& options) {
    int selected = 0;
    ChoiceLayout layout(width_, height_, static_cast<int>(options.size()));

    while (running_) {
        int mx, my;
        SDL_GetMouseState(&mx, &my);
        for (int i = 0; i < static_cast<int>(options.size()); ++i) {
            int iy = layout.item_y(i);
            if (mx >= layout.item_x && mx < layout.item_x + layout.item_w &&
                my >= iy && my < iy + layout.item_h) {
                selected = i;
                break;
            }
        }

        render_frame();
        render_choices(options, selected);
        SDL_RenderPresent(renderer_);

        SDL_Event event;
        while (SDL_PollEvent(&event)) {
            if (event.type == SDL_QUIT) {
                running_ = false;
                return {0, FlowSignal::Quit};
            }
            if (event.type == SDL_KEYDOWN) {
                switch (event.key.keysym.sym) {
                case SDLK_UP:
                    selected = (selected - 1 + static_cast<int>(options.size())) %
                               static_cast<int>(options.size());
                    break;
                case SDLK_DOWN:
                    selected = (selected + 1) % static_cast<int>(options.size());
                    break;
                case SDLK_RETURN:
                case SDLK_SPACE:
                    return {selected, FlowSignal::Continue};
                case SDLK_1: case SDLK_2: case SDLK_3: case SDLK_4:
                case SDLK_5: case SDLK_6: case SDLK_7: case SDLK_8: case SDLK_9: {
                    int idx = event.key.keysym.sym - SDLK_1;
                    if (idx >= 0 && idx < static_cast<int>(options.size())) {
                        return {idx, FlowSignal::Continue};
                    }
                    break;
                }
                default:
                    break;
                }
            }
            if (event.type == SDL_MOUSEBUTTONDOWN) {
                for (int i = 0; i < static_cast<int>(options.size()); ++i) {
                    int iy = layout.item_y(i);
                    if (event.button.x >= layout.item_x &&
                        event.button.x < layout.item_x + layout.item_w &&
                        event.button.y >= iy &&
                        event.button.y < iy + layout.item_h) {
                        return {i, FlowSignal::Continue};
                    }
                }
            }
        }
        SDL_Delay(16);
    }

    return {0, FlowSignal::Quit};
}

// ─── Scene / sprite management ───────────────────────────────────────────────

void SdlBackend::show_background(const std::string& image_path) {
    background_ = load_texture(image_path);
}

void SdlBackend::show_sprite(const std::string& tag, const std::string& image_path,
                              const std::string& position) {
    SDL_Texture* tex = load_texture(image_path);
    if (!tex) return;

    int w = 0, h = 0;
    SDL_QueryTexture(tex, nullptr, nullptr, &w, &h);

    float scale = static_cast<float>(height_) / static_cast<float>(h);
    if (scale > 1.5f) scale = 1.5f;

    sprites_[tag] = Sprite{tex, position, static_cast<int>(w * scale), static_cast<int>(h * scale)};
}

void SdlBackend::hide_sprite(const std::string& tag) {
    sprites_.erase(tag);
}

void SdlBackend::on_scene_changed(const std::string& /*room_id*/) {
    sprites_.clear();
}

// ─── Audio ───────────────────────────────────────────────────────────────────

void SdlBackend::play_music(const std::string& path, int fadein_ms, bool noloop, double volume) {
    if (path == current_music_path_ && Mix_PlayingMusic()) {
        if (volume >= 0.0) {
            music_volume_ = static_cast<int>(volume * MIX_MAX_VOLUME);
            Mix_VolumeMusic(music_volume_);
        }
        return;
    }

    Mix_HaltMusic();
    current_music_.reset();
    current_music_path_.clear();

    const std::string full_path = resolve_path(path);
    current_music_.reset(Mix_LoadMUS(full_path.c_str()));
    if (!current_music_) {
        std::cerr << "Failed to load music: " << full_path << " (" << Mix_GetError() << ")\n";
        return;
    }

    if (volume >= 0.0) {
        music_volume_ = static_cast<int>(volume * MIX_MAX_VOLUME);
    }
    Mix_VolumeMusic(music_volume_);

    int loops = noloop ? 0 : -1;
    int result;
    if (fadein_ms > 0) {
        result = Mix_FadeInMusic(current_music_.get(), loops, fadein_ms);
    } else {
        result = Mix_PlayMusic(current_music_.get(), loops);
    }

    if (result < 0) {
        std::cerr << "Failed to play music: " << Mix_GetError() << '\n';
        current_music_.reset();
        return;
    }
    current_music_path_ = path;
}

void SdlBackend::stop_music(int fadeout_ms) {
    if (!current_music_) return;

    if (fadeout_ms > 0) {
        Mix_FadeOutMusic(fadeout_ms);
    } else {
        Mix_HaltMusic();
        current_music_.reset();
    }
    current_music_path_.clear();
}

void SdlBackend::play_sound(const std::string& path, bool loop) {
    auto it = chunk_cache_.find(path);
    Mix_Chunk* chunk = nullptr;

    if (it != chunk_cache_.end()) {
        chunk = it->second.get();
    } else {
        const std::string full_path = resolve_path(path);
        chunk = Mix_LoadWAV(full_path.c_str());
        if (!chunk) {
            std::cerr << "Failed to load sound: " << full_path << " (" << Mix_GetError() << ")\n";
            return;
        }
        chunk_cache_[path] = sdl_raii::ChunkPtr(chunk);
    }

    Mix_VolumeChunk(chunk, sfx_volume_);
    int loops = loop ? -1 : 0;
    if (Mix_PlayChannel(-1, chunk, loops) < 0) {
        std::cerr << "Failed to play sound: " << Mix_GetError() << '\n';
    }
}

void SdlBackend::stop_sound() {
    Mix_HaltChannel(-1);
}

} // namespace novel::platform

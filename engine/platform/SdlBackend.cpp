#include "engine/platform/SdlBackend.hpp"

#include <SDL_mixer.h>

#include <algorithm>
#include <cmath>
#include <cstdlib>
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
    release_scene_target();

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
                    if (action == PauseAction::Save) {
                        return FlowSignal::SaveRequest;
                    }
                    if (action == PauseAction::Load) {
                        return FlowSignal::LoadRequest;
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
                    if (action == PauseAction::Save) return FlowSignal::SaveRequest;
                    if (action == PauseAction::Load) return FlowSignal::LoadRequest;
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
    background_path_ = image_path;
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

    sprites_[tag] = Sprite{tex, image_path, position, static_cast<int>(w * scale),
                           static_cast<int>(h * scale)};
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
    int channel = -1;
    for (int ch = 1; ch < 16; ++ch) {
        if (!Mix_Playing(ch)) {
            channel = ch;
            break;
        }
    }
    if (Mix_PlayChannel(channel, chunk, loops) < 0) {
        std::cerr << "Failed to play sound: " << Mix_GetError() << '\n';
    }
}

void SdlBackend::stop_sound() {
    for (int ch = 1; ch < 16; ++ch) {
        Mix_HaltChannel(ch);
    }
}

void SdlBackend::play_ambient(const std::string& path) {
    if (path == ambient_path_ && Mix_Playing(kAmbientChannel)) {
        return;
    }

    Mix_HaltChannel(kAmbientChannel);

    auto it = chunk_cache_.find(path);
    Mix_Chunk* chunk = nullptr;

    if (it != chunk_cache_.end()) {
        chunk = it->second.get();
    } else {
        const std::string full_path = resolve_path(path);
        chunk = Mix_LoadWAV(full_path.c_str());
        if (!chunk) {
            std::cerr << "Failed to load ambient: " << full_path << " (" << Mix_GetError() << ")\n";
            return;
        }
        chunk_cache_[path] = sdl_raii::ChunkPtr(chunk);
    }

    const int ambient_volume = std::max(sfx_volume_ / 3, MIX_MAX_VOLUME / 8);
    Mix_VolumeChunk(chunk, ambient_volume);
    if (Mix_PlayChannel(kAmbientChannel, chunk, -1) < 0) {
        std::cerr << "Failed to play ambient: " << Mix_GetError() << '\n';
        return;
    }
    ambient_path_ = path;
}

void SdlBackend::stop_ambient() {
    Mix_HaltChannel(kAmbientChannel);
    ambient_path_.clear();
}

void SdlBackend::ensure_scene_target() {
    if (scene_target_) {
        int tw = 0;
        int th = 0;
        SDL_QueryTexture(scene_target_, nullptr, nullptr, &tw, &th);
        if (tw == width_ && th == height_) {
            return;
        }
        release_scene_target();
    }

    scene_target_ = SDL_CreateTexture(renderer_, SDL_PIXELFORMAT_RGBA8888,
                                      SDL_TEXTUREACCESS_TARGET, width_, height_);
    if (!scene_target_) {
        std::cerr << "Failed to create scene target: " << SDL_GetError() << '\n';
    }
}

void SdlBackend::release_scene_target() {
    if (scene_target_) {
        SDL_DestroyTexture(scene_target_);
        scene_target_ = nullptr;
    }
}

void SdlBackend::capture_scene_to_target() {
    ensure_scene_target();
    if (!scene_target_) {
        return;
    }

    SDL_SetRenderTarget(renderer_, scene_target_);
    SDL_SetRenderDrawColor(renderer_, 0, 0, 0, 255);
    SDL_RenderClear(renderer_);
    render_background();
    render_sprites();
    SDL_SetRenderTarget(renderer_, nullptr);
}

void SdlBackend::blit_scene_normal() {
    if (!scene_target_) {
        render_background();
        render_sprites();
        return;
    }
    SDL_RenderCopy(renderer_, scene_target_, nullptr, nullptr);
}

void SdlBackend::render_tear_effect(float intensity) {
    if (!scene_target_) {
        return;
    }

    const int bands = std::max(4, 8 + static_cast<int>(intensity * 8.0f));
    const int band_h = std::max(1, height_ / bands);

    for (int i = 0; i < bands; ++i) {
        const int y = i * band_h;
        const int h = (i == bands - 1) ? height_ - y : band_h;
        const int offset = static_cast<int>((std::rand() % 41 - 20) * intensity * sx(2));
        const SDL_Rect src = {0, y, width_, h};
        const SDL_Rect dst = {offset, y, width_, h};
        SDL_RenderCopy(renderer_, scene_target_, &src, &dst);
    }
}

void SdlBackend::render_noise_overlay(float intensity) {
    SDL_SetRenderDrawBlendMode(renderer_, SDL_BLENDMODE_BLEND);
    const int count = std::max(20, static_cast<int>(width_ * height_ * intensity / 90.0f));

    for (int n = 0; n < count; ++n) {
        const int x = std::rand() % width_;
        const int y = std::rand() % height_;
        const Uint8 alpha = static_cast<Uint8>(80 + std::rand() % 120);
        SDL_SetRenderDrawColor(renderer_, std::rand() % 256, std::rand() % 256,
                               std::rand() % 256, alpha);
        const SDL_Rect rect = {x, y, 1 + std::rand() % std::max(2, sx(4)),
                               1 + std::rand() % std::max(2, sy(4))};
        SDL_RenderFillRect(renderer_, &rect);
    }
}

void SdlBackend::render_vignette_overlay(float intensity) {
    SDL_SetRenderDrawBlendMode(renderer_, SDL_BLENDMODE_BLEND);
    const Uint8 alpha = static_cast<Uint8>(std::min(220.0f, 100.0f + intensity * 120.0f));
    const int margin = static_cast<int>(sx(60) + intensity * sx(80));
    SDL_SetRenderDrawColor(renderer_, 0, 0, 0, alpha);

    const SDL_Rect top = {0, 0, width_, margin};
    const SDL_Rect bottom = {0, height_ - margin, width_, margin};
    const SDL_Rect left = {0, 0, margin, height_};
    const SDL_Rect right = {width_ - margin, 0, margin, height_};
    SDL_RenderFillRect(renderer_, &top);
    SDL_RenderFillRect(renderer_, &bottom);
    SDL_RenderFillRect(renderer_, &left);
    SDL_RenderFillRect(renderer_, &right);
}

void SdlBackend::render_invert_effect(float intensity) {
    if (!scene_target_) {
        return;
    }

    const int shift = std::max(1, static_cast<int>(sx(4) * intensity * (1 + std::rand() % 3)));

    SDL_SetTextureColorMod(scene_target_, 80, 255, 120);
    const SDL_Rect dst_green = {shift, 0, width_, height_};
    SDL_RenderCopy(renderer_, scene_target_, nullptr, &dst_green);

    SDL_SetTextureColorMod(scene_target_, 255, 80, 220);
    const SDL_Rect dst_magenta = {-shift, 0, width_, height_};
    SDL_RenderCopy(renderer_, scene_target_, nullptr, &dst_magenta);
    SDL_SetTextureColorMod(scene_target_, 255, 255, 255);

    if (intensity > 0.45f) {
        SDL_SetRenderDrawBlendMode(renderer_, SDL_BLENDMODE_BLEND);
        const Uint8 flash = static_cast<Uint8>(std::min(220.0f, (intensity - 0.45f) * 2.0f * 200.0f));
        SDL_SetRenderDrawColor(renderer_, 255, 255, 255, flash);
        const SDL_Rect full = {0, 0, width_, height_};
        SDL_RenderFillRect(renderer_, &full);
    }
}

void SdlBackend::glitch(const std::string& type, int duration_ms) {
    if (!renderer_ || duration_ms <= 0) {
        return;
    }

    capture_scene_to_target();
    const Uint32 end_time = SDL_GetTicks() + static_cast<Uint32>(duration_ms);

    while (running_ && SDL_GetTicks() < end_time) {
        const float elapsed = static_cast<float>(SDL_GetTicks() + duration_ms - end_time);
        const float progress = elapsed / static_cast<float>(duration_ms);
        const float intensity = 0.45f + 0.55f * std::fabs(std::sin(progress * 3.14159265f * 6.0f));

        SDL_SetRenderDrawColor(renderer_, 0, 0, 0, 255);
        SDL_RenderClear(renderer_);

        if (type == "tear") {
            render_tear_effect(intensity);
        } else if (type == "invert" || type == "color") {
            blit_scene_normal();
            render_invert_effect(intensity);
        } else if (type == "noise") {
            blit_scene_normal();
            render_noise_overlay(intensity);
        } else if (type == "vignette") {
            blit_scene_normal();
            render_vignette_overlay(intensity);
        } else {
            render_tear_effect(intensity * 0.7f);
            render_noise_overlay(intensity * 0.5f);
            render_vignette_overlay(intensity * 0.6f);
        }

        SDL_RenderPresent(renderer_);

        SDL_Event event;
        while (SDL_PollEvent(&event)) {
            if (event.type == SDL_QUIT) {
                running_ = false;
                return;
            }
        }
        SDL_Delay(16);
    }
}

void SdlBackend::set_window_title(const std::string& title) {
    if (window_) {
        SDL_SetWindowTitle(window_, title.c_str());
    }
}

void SdlBackend::reset_window_title() {
    set_window_title(title_);
}

std::string SdlBackend::current_background() const {
    return background_path_;
}

std::vector<core::GameSaveState::SpriteState> SdlBackend::current_sprites() const {
    std::vector<core::GameSaveState::SpriteState> sprites;
    sprites.reserve(sprites_.size());
    for (const auto& [tag, sprite] : sprites_) {
        core::GameSaveState::SpriteState state;
        state.tag = tag;
        state.path = sprite.image_path;
        state.position = sprite.position;
        sprites.push_back(std::move(state));
    }
    return sprites;
}

void SdlBackend::clear_sprites() {
    sprites_.clear();
}

void SdlBackend::fake_crash(const std::string& message) {
    if (!renderer_) {
        return;
    }

    glitch("noise", 120);

    SDL_SetRenderDrawColor(renderer_, 0, 0, 0, 255);
    SDL_RenderClear(renderer_);

    const std::string header = "ddlc_afterstory: fatal error";
    const std::string body = message.empty() ? "Segmentation fault (core dumped)" : message;
    const std::string footer = "Press any key to continue...";

    SDL_Color header_color = {220, 60, 60, 255};
    SDL_Color body_color = {230, 230, 230, 255};
    SDL_Color footer_color = {140, 140, 140, 255};

    int y = sy(80);
    if (font_small_) {
        SDL_Surface* header_surf = TTF_RenderUTF8_Blended(font_small_, header.c_str(), header_color);
        if (header_surf) {
            SDL_Texture* tex = SDL_CreateTextureFromSurface(renderer_, header_surf);
            SDL_Rect dst = {sx(60), y, header_surf->w, header_surf->h};
            SDL_RenderCopy(renderer_, tex, nullptr, &dst);
            SDL_DestroyTexture(tex);
            SDL_FreeSurface(header_surf);
            y += sy(40);
        }

        SDL_Surface* body_surf =
            TTF_RenderUTF8_Blended_Wrapped(font_small_, body.c_str(), body_color, width_ - sx(120));
        if (body_surf) {
            SDL_Texture* tex = SDL_CreateTextureFromSurface(renderer_, body_surf);
            SDL_Rect dst = {sx(60), y, body_surf->w, body_surf->h};
            SDL_RenderCopy(renderer_, tex, nullptr, &dst);
            SDL_DestroyTexture(tex);
            SDL_FreeSurface(body_surf);
            y += body_surf->h + sy(30);
        }

        SDL_Surface* footer_surf = TTF_RenderUTF8_Blended(font_small_, footer.c_str(), footer_color);
        if (footer_surf) {
            SDL_Texture* tex = SDL_CreateTextureFromSurface(renderer_, footer_surf);
            SDL_Rect dst = {sx(60), y, footer_surf->w, footer_surf->h};
            SDL_RenderCopy(renderer_, tex, nullptr, &dst);
            SDL_DestroyTexture(tex);
            SDL_FreeSurface(footer_surf);
        }
    }

    SDL_RenderPresent(renderer_);

    const Uint32 end_time = SDL_GetTicks() + 2500;
    bool dismissed = false;
    while (running_ && !dismissed && SDL_GetTicks() < end_time) {
        SDL_Event event;
        while (SDL_PollEvent(&event)) {
            if (event.type == SDL_QUIT) {
                running_ = false;
                return;
            }
            if (event.type == SDL_KEYDOWN || event.type == SDL_MOUSEBUTTONDOWN) {
                dismissed = true;
                break;
            }
        }
        SDL_Delay(16);
    }

    glitch("tear", 200);
    set_window_title(title_);
}

int SdlBackend::show_slot_menu(bool saving, const std::vector<core::SaveSlotInfo>& slots) {
    const std::string title = saving ? "Save Game" : "Load Game";
    const int count = static_cast<int>(slots.size());

    while (running_) {
        const int panel_w = sx(520);
        const int panel_h = sy(420);
        const int panel_x = (width_ - panel_w) / 2;
        const int panel_y = (height_ - panel_h) / 2;
        const int row_h = sy(64);
        const int row_spacing = sy(8);
        const int row_x = panel_x + sx(30);
        const int row_w = panel_w - sx(60);
        const int row_y_start = panel_y + sy(70);

        render_frame();

        SDL_SetRenderDrawBlendMode(renderer_, SDL_BLENDMODE_BLEND);
        SDL_SetRenderDrawColor(renderer_, 0, 0, 0, 170);
        SDL_Rect full = {0, 0, width_, height_};
        SDL_RenderFillRect(renderer_, &full);

        SDL_SetRenderDrawColor(renderer_, 20, 20, 40, 240);
        SDL_Rect panel = {panel_x, panel_y, panel_w, panel_h};
        SDL_RenderFillRect(renderer_, &panel);
        SDL_SetRenderDrawColor(renderer_, 180, 180, 220, 200);
        SDL_RenderDrawRect(renderer_, &panel);

        SDL_Color title_color = {255, 220, 230, 255};
        SDL_Surface* title_surf = TTF_RenderUTF8_Blended(font_, title.c_str(), title_color);
        if (title_surf) {
            SDL_Texture* title_tex = SDL_CreateTextureFromSurface(renderer_, title_surf);
            SDL_Rect title_dst = {panel_x + (panel_w - title_surf->w) / 2,
                                  panel_y + sy(18), title_surf->w, title_surf->h};
            SDL_RenderCopy(renderer_, title_tex, nullptr, &title_dst);
            SDL_DestroyTexture(title_tex);
            SDL_FreeSurface(title_surf);
        }

        int mx = 0;
        int my = 0;
        SDL_GetMouseState(&mx, &my);
        int hovered = -1;

        for (int i = 0; i < count; ++i) {
            const int row_y = row_y_start + i * (row_h + row_spacing);
            SDL_Rect row = {row_x, row_y, row_w, row_h};
            const bool hover = mx >= row.x && mx < row.x + row.w && my >= row.y && my < row.y + row.h;
            if (hover) {
                hovered = i;
            }

            SDL_SetRenderDrawColor(renderer_, hover ? 90 : 40, hover ? 35 : 25, hover ? 70 : 45, 230);
            SDL_RenderFillRect(renderer_, &row);

            std::string line = "Slot " + std::to_string(i + 1) + ": ";
            if (slots[static_cast<std::size_t>(i)].exists) {
                line += slots[static_cast<std::size_t>(i)].summary;
                if (!slots[static_cast<std::size_t>(i)].timestamp.empty()) {
                    line += " — " + slots[static_cast<std::size_t>(i)].timestamp;
                }
            } else {
                line += "Empty";
            }

            SDL_Color text_color = slots[static_cast<std::size_t>(i)].corrupted
                                       ? SDL_Color{255, 120, 140, 255}
                                       : SDL_Color{240, 240, 250, 255};
            SDL_Surface* line_surf =
                TTF_RenderUTF8_Blended_Wrapped(font_small_, line.c_str(), text_color,
                                               static_cast<Uint32>(row_w - sx(20)));
            if (line_surf) {
                SDL_Texture* line_tex = SDL_CreateTextureFromSurface(renderer_, line_surf);
                SDL_Rect line_dst = {row_x + sx(10), row_y + (row_h - line_surf->h) / 2,
                                     line_surf->w, line_surf->h};
                SDL_RenderCopy(renderer_, line_tex, nullptr, &line_dst);
                SDL_DestroyTexture(line_tex);
                SDL_FreeSurface(line_surf);
            }
        }

        SDL_RenderPresent(renderer_);

        SDL_Event event;
        while (SDL_PollEvent(&event)) {
            if (event.type == SDL_QUIT) {
                running_ = false;
                return -1;
            }
            if (event.type == SDL_KEYDOWN) {
                if (event.key.keysym.sym == SDLK_ESCAPE) {
                    return -1;
                }
                if (event.key.keysym.sym >= SDLK_1 && event.key.keysym.sym < SDLK_1 + count) {
                    const int slot = event.key.keysym.sym - SDLK_1;
                    if (!saving && !slots[static_cast<std::size_t>(slot)].exists) {
                        continue;
                    }
                    play_ui_sound("select.ogg");
                    return slot;
                }
            }
            if (event.type == SDL_MOUSEBUTTONDOWN && event.button.button == SDL_BUTTON_LEFT) {
                if (hovered >= 0) {
                    if (!saving && !slots[static_cast<std::size_t>(hovered)].exists) {
                        continue;
                    }
                    play_ui_sound("select.ogg");
                    return hovered;
                }
            }
        }
        SDL_Delay(16);
    }
    return -1;
}

} // namespace novel::platform

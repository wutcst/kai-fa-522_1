#include "engine/platform/SdlBackend.hpp"

#include <SDL_mixer.h>

#include <algorithm>
#include <filesystem>
#include <iostream>
#include <stdexcept>

namespace novel::platform {

SdlBackend::SdlBackend(int width, int height, const std::string& title,
                         const std::string& content_root)
    : width_(width), height_(height), title_(title), content_root_(content_root) {}

SdlBackend::~SdlBackend() { shutdown(); }

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

    const std::string font_path = resolve_path("fonts/default.ttf");
    font_ = TTF_OpenFont(font_path.c_str(), 24);
    if (!font_) {
        font_ = TTF_OpenFont("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 24);
    }
    if (!font_) {
        std::cerr << "TTF_OpenFont failed: " << TTF_GetError() << '\n';
        return false;
    }

    font_small_ = TTF_OpenFont(font_path.c_str(), 20);
    if (!font_small_) {
        font_small_ = TTF_OpenFont("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 20);
    }
    if (!font_small_) {
        font_small_ = font_;
    }

    const std::string title_font_path = resolve_path("gui/font/RifficFree-Bold.ttf");
    font_title_ = TTF_OpenFont(title_font_path.c_str(), 48);
    if (!font_title_) {
        font_title_ = font_;
    }

    running_ = true;
    return true;
}

void SdlBackend::shutdown() {
    Mix_HaltChannel(-1);
    if (current_music_) {
        Mix_HaltMusic();
        Mix_FreeMusic(current_music_);
        current_music_ = nullptr;
    }
    for (auto& [_, chunk] : chunk_cache_) {
        Mix_FreeChunk(chunk);
    }
    chunk_cache_.clear();
    Mix_CloseAudio();

    for (auto& [_, tex] : texture_cache_) {
        if (tex) SDL_DestroyTexture(tex);
    }
    texture_cache_.clear();
    sprites_.clear();
    background_ = nullptr;

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
        return it->second;
    }

    const std::string full_path = resolve_path(path);
    SDL_Surface* surface = IMG_Load(full_path.c_str());
    if (!surface) {
        std::cerr << "Failed to load image: " << full_path << " (" << IMG_GetError() << ")\n";
        return nullptr;
    }

    SDL_Texture* texture = SDL_CreateTextureFromSurface(renderer_, surface);
    SDL_FreeSurface(surface);
    texture_cache_[path] = texture;
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
    const int box_height = 185;
    const int box_y = height_ - box_height;
    const int padding = 40;

    SDL_Texture* tb_tex = load_texture("gui/textbox.png");
    if (tb_tex) {
        int tw, th;
        SDL_QueryTexture(tb_tex, nullptr, nullptr, &tw, &th);
        float scale = static_cast<float>(width_) * 0.8f / static_cast<float>(tw);
        int draw_w = static_cast<int>(tw * scale);
        int draw_h = static_cast<int>(th * scale);
        SDL_Rect tb_dst = {(width_ - draw_w) / 2, height_ - draw_h - 10, draw_w, draw_h};
        SDL_RenderCopy(renderer_, tb_tex, nullptr, &tb_dst);
    } else {
        SDL_SetRenderDrawBlendMode(renderer_, SDL_BLENDMODE_BLEND);
        SDL_SetRenderDrawColor(renderer_, 0, 0, 0, 200);
        SDL_Rect box = {0, box_y, width_, box_height};
        SDL_RenderFillRect(renderer_, &box);
        SDL_SetRenderDrawColor(renderer_, 200, 200, 200, 255);
        SDL_RenderDrawRect(renderer_, &box);
    }

    const int text_left = width_ / 8;
    int text_y = height_ - box_height + 30;

    if (!speaker.empty()) {
        SDL_Color name_color = {255, 182, 193, 255};
        SDL_Surface* name_surface = TTF_RenderUTF8_Blended(font_, speaker.c_str(), name_color);
        if (name_surface) {
            SDL_Texture* name_tex = SDL_CreateTextureFromSurface(renderer_, name_surface);
            SDL_Rect name_rect = {text_left, text_y, name_surface->w, name_surface->h};
            SDL_RenderCopy(renderer_, name_tex, nullptr, &name_rect);
            text_y += name_surface->h + 6;
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

    const int item_h = 54;
    const int item_spacing = 8;
    const int item_w = width_ * 3 / 5;
    const int item_x = (width_ - item_w) / 2;
    const int total_h = static_cast<int>(options.size()) * (item_h + item_spacing) - item_spacing;
    int start_y = (height_ - total_h) / 2;

    for (int i = 0; i < static_cast<int>(options.size()); ++i) {
        int item_y = start_y + i * (item_h + item_spacing);
        SDL_Rect dst = {item_x, item_y, item_w, item_h};

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
                                           : SDL_Color{255, 255, 255, 255};
        const std::string label = options[static_cast<std::size_t>(i)];
        SDL_Surface* surface = TTF_RenderUTF8_Blended_Wrapped(
            font_, label.c_str(), color, static_cast<Uint32>(item_w - 40));
        if (surface) {
            SDL_Texture* tex = SDL_CreateTextureFromSurface(renderer_, surface);
            SDL_Rect text_dst = {item_x + 20, item_y + (item_h - surface->h) / 2,
                                 surface->w, surface->h};
            SDL_RenderCopy(renderer_, tex, nullptr, &text_dst);
            SDL_DestroyTexture(tex);
            SDL_FreeSurface(surface);
        }
    }
}

void SdlBackend::wait_for_advance() {
    SDL_RenderPresent(renderer_);

    while (running_) {
        SDL_Event event;
        while (SDL_PollEvent(&event)) {
            if (event.type == SDL_QUIT) {
                running_ = false;
                throw std::runtime_error("quit");
            }
            if (event.type == SDL_KEYDOWN) {
                if (event.key.keysym.sym == SDLK_RETURN || event.key.keysym.sym == SDLK_SPACE) {
                    return;
                }
                if (event.key.keysym.sym == SDLK_ESCAPE) {
                    GameSettings settings;
                    settings.music_volume = music_volume_ * 100 / MIX_MAX_VOLUME;
                    settings.sfx_volume = sfx_volume_ * 100 / MIX_MAX_VOLUME;
                    PauseAction action = show_pause_menu();
                    if (action == PauseAction::Settings) {
                        show_settings(settings);
                    } else if (action == PauseAction::MainMenu) {
                        throw std::runtime_error("main_menu");
                    }
                    render_frame();
                    render_textbox("", "");
                    SDL_RenderPresent(renderer_);
                }
            }
            if (event.type == SDL_MOUSEBUTTONDOWN) {
                return;
            }
        }
        SDL_Delay(16);
    }
}

void SdlBackend::say(const std::string& speaker, const std::string& text) {
    render_frame();
    render_textbox(speaker, text);
    wait_for_advance();
}

int SdlBackend::choose(const std::vector<std::string>& options) {
    int selected = 0;

    const int item_h = 54;
    const int item_spacing = 8;
    const int item_w = width_ * 3 / 5;
    const int item_x = (width_ - item_w) / 2;
    const int total_h = static_cast<int>(options.size()) * (item_h + item_spacing) - item_spacing;
    const int start_y = (height_ - total_h) / 2;

    while (running_) {
        // Track mouse hover for highlight
        int mx, my;
        SDL_GetMouseState(&mx, &my);
        for (int i = 0; i < static_cast<int>(options.size()); ++i) {
            int iy = start_y + i * (item_h + item_spacing);
            if (mx >= item_x && mx < item_x + item_w && my >= iy && my < iy + item_h) {
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
                throw std::runtime_error("quit");
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
                    return selected;
                case SDLK_1: case SDLK_2: case SDLK_3: case SDLK_4:
                case SDLK_5: case SDLK_6: case SDLK_7: case SDLK_8: case SDLK_9: {
                    int idx = event.key.keysym.sym - SDLK_1;
                    if (idx >= 0 && idx < static_cast<int>(options.size())) {
                        return idx;
                    }
                    break;
                }
                default:
                    break;
                }
            }
            if (event.type == SDL_MOUSEBUTTONDOWN) {
                const int item_h = 54;
                const int item_spacing = 8;
                const int item_w = width_ * 3 / 5;
                const int item_x = (width_ - item_w) / 2;
                const int total_h = static_cast<int>(options.size()) * (item_h + item_spacing) - item_spacing;
                int start_y = (height_ - total_h) / 2;

                for (int i = 0; i < static_cast<int>(options.size()); ++i) {
                    int iy = start_y + i * (item_h + item_spacing);
                    if (event.button.x >= item_x && event.button.x < item_x + item_w &&
                        event.button.y >= iy && event.button.y < iy + item_h) {
                        return i;
                    }
                }
            }
        }
        SDL_Delay(16);
    }

    return 0;
}

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

void SdlBackend::play_music(const std::string& path, int fadein_ms, bool noloop, double volume) {
    if (path == current_music_path_ && Mix_PlayingMusic()) {
        if (volume >= 0.0) {
            music_volume_ = static_cast<int>(volume * MIX_MAX_VOLUME);
            Mix_VolumeMusic(music_volume_);
        }
        return;
    }

    Mix_HaltMusic();
    if (current_music_) {
        Mix_FreeMusic(current_music_);
        current_music_ = nullptr;
        current_music_path_.clear();
    }

    const std::string full_path = resolve_path(path);
    current_music_ = Mix_LoadMUS(full_path.c_str());
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
        result = Mix_FadeInMusic(current_music_, loops, fadein_ms);
    } else {
        result = Mix_PlayMusic(current_music_, loops);
    }

    if (result < 0) {
        std::cerr << "Failed to play music: " << Mix_GetError() << '\n';
        Mix_FreeMusic(current_music_);
        current_music_ = nullptr;
        return;
    }
    current_music_path_ = path;
}

void SdlBackend::stop_music(int fadeout_ms) {
    if (!current_music_) return;

    if (fadeout_ms > 0) {
        Mix_FadeOutMusic(fadeout_ms);
        // Music will be freed on next play_music call or shutdown.
        // Don't free now—Mix_FreeMusic would halt the fade immediately.
    } else {
        Mix_HaltMusic();
        Mix_FreeMusic(current_music_);
        current_music_ = nullptr;
    }
    current_music_path_.clear();
}

void SdlBackend::play_sound(const std::string& path, bool loop) {
    auto it = chunk_cache_.find(path);
    Mix_Chunk* chunk = nullptr;

    if (it != chunk_cache_.end()) {
        chunk = it->second;
    } else {
        const std::string full_path = resolve_path(path);
        chunk = Mix_LoadWAV(full_path.c_str());
        if (!chunk) {
            std::cerr << "Failed to load sound: " << full_path << " (" << Mix_GetError() << ")\n";
            return;
        }
        chunk_cache_[path] = chunk;
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

// ─── UI Helper Methods ───────────────────────────────────────────────────────

void SdlBackend::play_ui_sound(const std::string& name) {
    play_sound("gui/" + name, false);
}

bool SdlBackend::render_button(Button& btn, TTF_Font* font) {
    int mx, my;
    Uint32 mouse = SDL_GetMouseState(&mx, &my);
    bool was_hovered = btn.hovered;
    btn.hovered = (mx >= btn.rect.x && mx < btn.rect.x + btn.rect.w &&
                   my >= btn.rect.y && my < btn.rect.y + btn.rect.h);

    if (btn.hovered && !was_hovered) {
        play_ui_sound("hover.ogg");
    }

    SDL_SetRenderDrawBlendMode(renderer_, SDL_BLENDMODE_BLEND);
    if (btn.hovered) {
        SDL_SetRenderDrawColor(renderer_, 255, 120, 150, 240);
    } else {
        SDL_SetRenderDrawColor(renderer_, 30, 20, 40, 200);
    }
    SDL_RenderFillRect(renderer_, &btn.rect);

    SDL_SetRenderDrawColor(renderer_, 255, 200, 210, 200);
    SDL_RenderDrawRect(renderer_, &btn.rect);

    SDL_Color text_color = btn.hovered ? SDL_Color{255, 255, 255, 255}
                                       : SDL_Color{255, 220, 230, 255};
    SDL_Surface* surface = TTF_RenderUTF8_Blended(font, btn.label.c_str(), text_color);
    if (surface) {
        SDL_Texture* tex = SDL_CreateTextureFromSurface(renderer_, surface);
        SDL_Rect dst = {btn.rect.x + (btn.rect.w - surface->w) / 2,
                        btn.rect.y + (btn.rect.h - surface->h) / 2,
                        surface->w, surface->h};
        SDL_RenderCopy(renderer_, tex, nullptr, &dst);
        SDL_DestroyTexture(tex);
        SDL_FreeSurface(surface);
    }

    bool clicked = btn.hovered && (mouse & SDL_BUTTON(SDL_BUTTON_LEFT));
    return clicked;
}

void SdlBackend::render_slider(int x, int y, int w, int value, bool active) {
    const int bar_h = 6;
    const int thumb_w = 16;
    const int thumb_h = 24;

    SDL_Rect bar_rect = {x, y + thumb_h / 2 - bar_h / 2, w, bar_h};
    SDL_SetRenderDrawColor(renderer_, 100, 100, 100, 200);
    SDL_RenderFillRect(renderer_, &bar_rect);

    int fill_w = value * w / 100;
    SDL_Rect fill_rect = {x, bar_rect.y, fill_w, bar_h};
    if (active) {
        SDL_SetRenderDrawColor(renderer_, 255, 150, 180, 255);
    } else {
        SDL_SetRenderDrawColor(renderer_, 180, 180, 180, 255);
    }
    SDL_RenderFillRect(renderer_, &fill_rect);

    int thumb_x = x + fill_w - thumb_w / 2;
    SDL_Rect thumb_rect = {thumb_x, y, thumb_w, thumb_h};
    SDL_SetRenderDrawColor(renderer_, 255, 255, 255, 255);
    SDL_RenderFillRect(renderer_, &thumb_rect);
}

// ─── Main Menu ───────────────────────────────────────────────────────────────

MenuAction SdlBackend::show_main_menu() {
    SDL_Texture* bg_tex = load_texture("gui/menu_bg.png");
    SDL_Texture* overlay_tex = load_texture("gui/overlay/main_menu.png");
    SDL_Texture* logo_tex = load_texture("gui/logo.png");

    // DDLC original layout (1280x720 reference):
    //   Yuri:    xcenter 600, ycenter 335, zoom 0.60
    //   Natsuki: xcenter 750, ycenter 385, zoom 0.58
    //   Sayori:  xcenter 510, ycenter 500, zoom 0.68
    //   Monika:  xcenter 1000, ycenter 640, zoom 1.00
    // Layer order: bg → Yuri → Natsuki → overlay → Sayori → Monika → logo → buttons

    struct CharDef { const char* path; float xcenter; float ycenter; float zoom; };
    CharDef char_defs[] = {
        {"gui/menu_art_y.png", 600.0f / 1280, 335.0f / 720, 0.60f},
        {"gui/menu_art_n.png", 750.0f / 1280, 385.0f / 720, 0.58f},
    };
    CharDef char_front[] = {
        {"gui/menu_art_s.png", 510.0f / 1280, 500.0f / 720, 0.68f},
        {"gui/menu_art_m.png", 1000.0f / 1280, 640.0f / 720, 1.00f},
    };

    SDL_Texture* back_chars[2] = {
        load_texture(char_defs[0].path),
        load_texture(char_defs[1].path),
    };
    SDL_Texture* front_chars[2] = {
        load_texture(char_front[0].path),
        load_texture(char_front[1].path),
    };

    const int btn_w = 200;
    const int btn_h = 44;
    const int btn_spacing = 12;
    const int btn_x = 60;
    const int btn_start_y = height_ / 2 + 40;

    Button buttons[3];
    buttons[0] = {{btn_x, btn_start_y, btn_w, btn_h}, "New Game"};
    buttons[1] = {{btn_x, btn_start_y + btn_h + btn_spacing, btn_w, btn_h}, "Settings"};
    buttons[2] = {{btn_x, btn_start_y + (btn_h + btn_spacing) * 2, btn_w, btn_h}, "Quit"};

    auto draw_char = [&](SDL_Texture* tex, float xc, float yc, float zoom) {
        if (!tex) return;
        int tw, th;
        SDL_QueryTexture(tex, nullptr, nullptr, &tw, &th);
        int draw_w = static_cast<int>(tw * zoom);
        int draw_h = static_cast<int>(th * zoom);
        int dx = static_cast<int>(xc * width_) - draw_w / 2;
        int dy = static_cast<int>(yc * height_) - draw_h / 2;
        SDL_Rect dst = {dx, dy, draw_w, draw_h};
        SDL_RenderCopy(renderer_, tex, nullptr, &dst);
    };

    bool clicked_last_frame = false;

    while (running_) {
        SDL_SetRenderDrawColor(renderer_, 0, 0, 0, 255);
        SDL_RenderClear(renderer_);

        // Layer 1: Background (stretch to fill)
        if (bg_tex) SDL_RenderCopy(renderer_, bg_tex, nullptr, nullptr);

        // Layer 2: Back characters (Yuri, Natsuki)
        for (int i = 0; i < 2; ++i) {
            draw_char(back_chars[i], char_defs[i].xcenter, char_defs[i].ycenter, char_defs[i].zoom);
        }

        // Layer 3: Right-side navigation overlay
        if (overlay_tex) SDL_RenderCopy(renderer_, overlay_tex, nullptr, nullptr);

        // Layer 4: Front characters (Sayori, Monika)
        for (int i = 0; i < 2; ++i) {
            draw_char(front_chars[i], char_front[i].xcenter, char_front[i].ycenter, char_front[i].zoom);
        }

        // Layer 5: Logo (top-left)
        if (logo_tex) {
            int lw, lh;
            SDL_QueryTexture(logo_tex, nullptr, nullptr, &lw, &lh);
            float scale = 240.0f / static_cast<float>(lw);
            int logo_draw_w = static_cast<int>(lw * scale);
            int logo_draw_h = static_cast<int>(lh * scale);
            SDL_Rect logo_dst = {40, 24, logo_draw_w, logo_draw_h};
            SDL_RenderCopy(renderer_, logo_tex, nullptr, &logo_dst);
        }

        // Layer 6: Buttons
        for (auto& btn : buttons) {
            render_button(btn, font_);
        }

        SDL_RenderPresent(renderer_);

        SDL_Event event;
        while (SDL_PollEvent(&event)) {
            if (event.type == SDL_QUIT) {
                running_ = false;
                return MenuAction::Quit;
            }
            if (event.type == SDL_MOUSEBUTTONDOWN && event.button.button == SDL_BUTTON_LEFT) {
                if (!clicked_last_frame) {
                    for (int i = 0; i < 3; ++i) {
                        if (buttons[i].hovered) {
                            play_ui_sound("select.ogg");
                            switch (i) {
                            case 0: return MenuAction::NewGame;
                            case 1: return MenuAction::Settings;
                            case 2: return MenuAction::Quit;
                            }
                        }
                    }
                }
                clicked_last_frame = true;
            }
            if (event.type == SDL_MOUSEBUTTONUP) {
                clicked_last_frame = false;
            }
            if (event.type == SDL_KEYDOWN) {
                if (event.key.keysym.sym == SDLK_RETURN || event.key.keysym.sym == SDLK_SPACE) {
                    return MenuAction::NewGame;
                }
                if (event.key.keysym.sym == SDLK_ESCAPE) {
                    return MenuAction::Quit;
                }
            }
        }
        SDL_Delay(16);
    }
    return MenuAction::Quit;
}

// ─── Settings Screen ─────────────────────────────────────────────────────────

void SdlBackend::show_settings(GameSettings& settings) {
    SDL_Texture* bg_tex = load_texture("gui/menu_bg.png");
    SDL_Texture* overlay_tex = load_texture("gui/overlay/game_menu.png");

    const int panel_w = 600;
    const int panel_h = 400;
    const int panel_x = (width_ - panel_w) / 2;
    const int panel_y = (height_ - panel_h) / 2;
    const int label_x = panel_x + 40;
    const int slider_x = panel_x + 200;
    const int slider_w = 320;
    const int row_h = 60;

    Button back_btn = {{panel_x + panel_w / 2 - 80, panel_y + panel_h - 60, 160, 44}, "Back"};

    int dragging = -1;  // which slider is being dragged (-1 = none)

    while (running_) {
        SDL_SetRenderDrawColor(renderer_, 0, 0, 0, 255);
        SDL_RenderClear(renderer_);
        if (bg_tex) SDL_RenderCopy(renderer_, bg_tex, nullptr, nullptr);
        if (overlay_tex) SDL_RenderCopy(renderer_, overlay_tex, nullptr, nullptr);

        // Panel background
        SDL_SetRenderDrawBlendMode(renderer_, SDL_BLENDMODE_BLEND);
        SDL_SetRenderDrawColor(renderer_, 20, 20, 40, 220);
        SDL_Rect panel = {panel_x, panel_y, panel_w, panel_h};
        SDL_RenderFillRect(renderer_, &panel);
        SDL_SetRenderDrawColor(renderer_, 200, 200, 255, 180);
        SDL_RenderDrawRect(renderer_, &panel);

        // Title
        SDL_Color title_col = {255, 255, 255, 255};
        SDL_Surface* title_surf = TTF_RenderUTF8_Blended(font_title_, "Settings", title_col);
        if (title_surf) {
            SDL_Texture* title_tex = SDL_CreateTextureFromSurface(renderer_, title_surf);
            SDL_Rect title_dst = {panel_x + (panel_w - title_surf->w) / 2,
                                  panel_y + 16, title_surf->w, title_surf->h};
            SDL_RenderCopy(renderer_, title_tex, nullptr, &title_dst);
            SDL_DestroyTexture(title_tex);
            SDL_FreeSurface(title_surf);
        }

        int base_y = panel_y + 90;
        struct SliderRow { const char* label; int* value; };
        SliderRow rows[] = {
            {"Music Volume", &settings.music_volume},
            {"SFX Volume", &settings.sfx_volume},
            {"Text Speed", &settings.text_speed},
        };

        int mx, my;
        SDL_GetMouseState(&mx, &my);

        for (int i = 0; i < 3; ++i) {
            int row_y = base_y + i * row_h;
            SDL_Color lbl_col = {220, 220, 220, 255};
            SDL_Surface* lbl_surf = TTF_RenderUTF8_Blended(font_, rows[i].label, lbl_col);
            if (lbl_surf) {
                SDL_Texture* lbl_tex = SDL_CreateTextureFromSurface(renderer_, lbl_surf);
                SDL_Rect lbl_dst = {label_x, row_y + 4, lbl_surf->w, lbl_surf->h};
                SDL_RenderCopy(renderer_, lbl_tex, nullptr, &lbl_dst);
                SDL_DestroyTexture(lbl_tex);
                SDL_FreeSurface(lbl_surf);
            }

            bool active = (dragging == i);
            render_slider(slider_x, row_y, slider_w, *rows[i].value, active);

            if (dragging == i) {
                int new_val = (mx - slider_x) * 100 / slider_w;
                if (new_val < 0) new_val = 0;
                if (new_val > 100) new_val = 100;
                *rows[i].value = new_val;
            }

            // Value text
            std::string val_str = std::to_string(*rows[i].value) + "%";
            SDL_Color val_col = {200, 200, 200, 255};
            SDL_Surface* val_surf = TTF_RenderUTF8_Blended(font_small_, val_str.c_str(), val_col);
            if (val_surf) {
                SDL_Texture* val_tex = SDL_CreateTextureFromSurface(renderer_, val_surf);
                SDL_Rect val_dst = {slider_x + slider_w + 12, row_y + 4,
                                    val_surf->w, val_surf->h};
                SDL_RenderCopy(renderer_, val_tex, nullptr, &val_dst);
                SDL_DestroyTexture(val_tex);
                SDL_FreeSurface(val_surf);
            }
        }

        // Fullscreen toggle
        int fs_y = base_y + 3 * row_h;
        SDL_Color fs_col = {220, 220, 220, 255};
        std::string fs_label = std::string("Fullscreen: ") + (settings.fullscreen ? "ON" : "OFF");
        SDL_Surface* fs_surf = TTF_RenderUTF8_Blended(font_, fs_label.c_str(), fs_col);
        if (fs_surf) {
            SDL_Texture* fs_tex = SDL_CreateTextureFromSurface(renderer_, fs_surf);
            SDL_Rect fs_dst = {label_x, fs_y + 4, fs_surf->w, fs_surf->h};
            SDL_RenderCopy(renderer_, fs_tex, nullptr, &fs_dst);
            SDL_DestroyTexture(fs_tex);
            SDL_FreeSurface(fs_surf);
        }

        render_button(back_btn, font_);
        SDL_RenderPresent(renderer_);

        SDL_Event event;
        while (SDL_PollEvent(&event)) {
            if (event.type == SDL_QUIT) {
                running_ = false;
                return;
            }
            if (event.type == SDL_KEYDOWN && event.key.keysym.sym == SDLK_ESCAPE) {
                apply_settings(settings);
                return;
            }
            if (event.type == SDL_MOUSEBUTTONDOWN && event.button.button == SDL_BUTTON_LEFT) {
                // Check sliders
                for (int i = 0; i < 3; ++i) {
                    int row_y = base_y + i * row_h;
                    SDL_Rect slider_area = {slider_x, row_y, slider_w, 30};
                    if (mx >= slider_area.x && mx < slider_area.x + slider_area.w &&
                        my >= slider_area.y && my < slider_area.y + slider_area.h) {
                        dragging = i;
                    }
                }
                // Check fullscreen toggle
                if (mx >= label_x && mx < label_x + 300 &&
                    my >= fs_y && my < fs_y + 36) {
                    settings.fullscreen = !settings.fullscreen;
                    apply_settings(settings);
                }
                // Check back button
                if (back_btn.hovered) {
                    play_ui_sound("select.ogg");
                    apply_settings(settings);
                    return;
                }
            }
            if (event.type == SDL_MOUSEBUTTONUP) {
                dragging = -1;
            }
        }
        SDL_Delay(16);
    }
}

// ─── Pause Menu ──────────────────────────────────────────────────────────────

PauseAction SdlBackend::show_pause_menu() {
    const int panel_w = 300;
    const int panel_h = 260;
    const int panel_x = (width_ - panel_w) / 2;
    const int panel_y = (height_ - panel_h) / 2;

    const int btn_w = 200;
    const int btn_h = 44;
    const int btn_spacing = 14;
    const int btn_x = panel_x + (panel_w - btn_w) / 2;
    int btn_y_start = panel_y + 70;

    Button buttons[3];
    buttons[0] = {{btn_x, btn_y_start, btn_w, btn_h}, "Resume"};
    buttons[1] = {{btn_x, btn_y_start + btn_h + btn_spacing, btn_w, btn_h}, "Settings"};
    buttons[2] = {{btn_x, btn_y_start + (btn_h + btn_spacing) * 2, btn_w, btn_h}, "Main Menu"};

    while (running_) {
        render_frame();

        // Dim overlay
        SDL_SetRenderDrawBlendMode(renderer_, SDL_BLENDMODE_BLEND);
        SDL_SetRenderDrawColor(renderer_, 0, 0, 0, 150);
        SDL_Rect full = {0, 0, width_, height_};
        SDL_RenderFillRect(renderer_, &full);

        // Panel
        SDL_SetRenderDrawColor(renderer_, 20, 20, 40, 230);
        SDL_Rect panel = {panel_x, panel_y, panel_w, panel_h};
        SDL_RenderFillRect(renderer_, &panel);
        SDL_SetRenderDrawColor(renderer_, 180, 180, 220, 200);
        SDL_RenderDrawRect(renderer_, &panel);

        // Title
        SDL_Color title_col = {255, 255, 255, 255};
        SDL_Surface* title_surf = TTF_RenderUTF8_Blended(font_, "Paused", title_col);
        if (title_surf) {
            SDL_Texture* title_tex = SDL_CreateTextureFromSurface(renderer_, title_surf);
            SDL_Rect title_dst = {panel_x + (panel_w - title_surf->w) / 2,
                                  panel_y + 20, title_surf->w, title_surf->h};
            SDL_RenderCopy(renderer_, title_tex, nullptr, &title_dst);
            SDL_DestroyTexture(title_tex);
            SDL_FreeSurface(title_surf);
        }

        for (auto& btn : buttons) {
            render_button(btn, font_);
        }

        SDL_RenderPresent(renderer_);

        SDL_Event event;
        while (SDL_PollEvent(&event)) {
            if (event.type == SDL_QUIT) {
                running_ = false;
                throw std::runtime_error("quit");
            }
            if (event.type == SDL_KEYDOWN && event.key.keysym.sym == SDLK_ESCAPE) {
                return PauseAction::Resume;
            }
            if (event.type == SDL_MOUSEBUTTONDOWN && event.button.button == SDL_BUTTON_LEFT) {
                for (int i = 0; i < 3; ++i) {
                    if (buttons[i].hovered) {
                        play_ui_sound("select.ogg");
                        switch (i) {
                        case 0: return PauseAction::Resume;
                        case 1: return PauseAction::Settings;
                        case 2: return PauseAction::MainMenu;
                        }
                    }
                }
            }
        }
        SDL_Delay(16);
    }
    return PauseAction::Resume;
}

// ─── Apply Settings ──────────────────────────────────────────────────────────

void SdlBackend::apply_settings(const GameSettings& settings) {
    music_volume_ = settings.music_volume * MIX_MAX_VOLUME / 100;
    sfx_volume_ = settings.sfx_volume * MIX_MAX_VOLUME / 100;
    Mix_VolumeMusic(music_volume_);

    if (window_) {
        Uint32 flags = SDL_GetWindowFlags(window_);
        bool is_fs = (flags & SDL_WINDOW_FULLSCREEN_DESKTOP) != 0;
        if (settings.fullscreen != is_fs) {
            SDL_SetWindowFullscreen(window_,
                settings.fullscreen ? SDL_WINDOW_FULLSCREEN_DESKTOP : 0);
        }
    }
}

} // namespace novel::platform

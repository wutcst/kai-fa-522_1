#include "engine/platform/SdlBackend.hpp"

#include <SDL_mixer.h>

#include <iostream>
#include <stdexcept>
#include <string>

namespace novel::platform {

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

        if (bg_tex) SDL_RenderCopy(renderer_, bg_tex, nullptr, nullptr);

        for (int i = 0; i < 2; ++i) {
            draw_char(back_chars[i], char_defs[i].xcenter, char_defs[i].ycenter, char_defs[i].zoom);
        }

        if (overlay_tex) SDL_RenderCopy(renderer_, overlay_tex, nullptr, nullptr);

        for (int i = 0; i < 2; ++i) {
            draw_char(front_chars[i], char_front[i].xcenter, char_front[i].ycenter, char_front[i].zoom);
        }

        if (logo_tex) {
            int lw, lh;
            SDL_QueryTexture(logo_tex, nullptr, nullptr, &lw, &lh);
            float scale = 240.0f / static_cast<float>(lw);
            int logo_draw_w = static_cast<int>(lw * scale);
            int logo_draw_h = static_cast<int>(lh * scale);
            SDL_Rect logo_dst = {40, 24, logo_draw_w, logo_draw_h};
            SDL_RenderCopy(renderer_, logo_tex, nullptr, &logo_dst);
        }

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

    int dragging = -1;

    while (running_) {
        SDL_SetRenderDrawColor(renderer_, 0, 0, 0, 255);
        SDL_RenderClear(renderer_);
        if (bg_tex) SDL_RenderCopy(renderer_, bg_tex, nullptr, nullptr);
        if (overlay_tex) SDL_RenderCopy(renderer_, overlay_tex, nullptr, nullptr);

        SDL_SetRenderDrawBlendMode(renderer_, SDL_BLENDMODE_BLEND);
        SDL_SetRenderDrawColor(renderer_, 20, 20, 40, 220);
        SDL_Rect panel = {panel_x, panel_y, panel_w, panel_h};
        SDL_RenderFillRect(renderer_, &panel);
        SDL_SetRenderDrawColor(renderer_, 200, 200, 255, 180);
        SDL_RenderDrawRect(renderer_, &panel);

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
                for (int i = 0; i < 3; ++i) {
                    int row_y = base_y + i * row_h;
                    SDL_Rect slider_area = {slider_x, row_y, slider_w, 30};
                    if (mx >= slider_area.x && mx < slider_area.x + slider_area.w &&
                        my >= slider_area.y && my < slider_area.y + slider_area.h) {
                        dragging = i;
                    }
                }
                if (mx >= label_x && mx < label_x + 300 &&
                    my >= fs_y && my < fs_y + 36) {
                    settings.fullscreen = !settings.fullscreen;
                    apply_settings(settings);
                }
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

        SDL_SetRenderDrawBlendMode(renderer_, SDL_BLENDMODE_BLEND);
        SDL_SetRenderDrawColor(renderer_, 0, 0, 0, 150);
        SDL_Rect full = {0, 0, width_, height_};
        SDL_RenderFillRect(renderer_, &full);

        SDL_SetRenderDrawColor(renderer_, 20, 20, 40, 230);
        SDL_Rect panel = {panel_x, panel_y, panel_w, panel_h};
        SDL_RenderFillRect(renderer_, &panel);
        SDL_SetRenderDrawColor(renderer_, 180, 180, 220, 200);
        SDL_RenderDrawRect(renderer_, &panel);

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

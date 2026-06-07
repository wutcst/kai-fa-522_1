#pragma once

#include "engine/platform/IBackend.hpp"

#include <SDL.h>
#include <SDL_image.h>
#include <SDL_mixer.h>
#include <SDL_ttf.h>

#include <string>
#include <unordered_map>
#include <vector>

namespace novel::platform {

struct Sprite {
    SDL_Texture* texture = nullptr;
    std::string position;
    int w = 0;
    int h = 0;
};

/// SDL2-based graphical backend for visual novel rendering.
class SdlBackend final : public IBackend {
public:
    SdlBackend(int width, int height, const std::string& title,
               const std::string& content_root);
    ~SdlBackend() override;

    bool init() override;
    void shutdown() override;

    void say(const std::string& speaker, const std::string& text) override;
    int choose(const std::vector<std::string>& options) override;
    void show_background(const std::string& image_path) override;
    void show_sprite(const std::string& tag, const std::string& image_path,
                     const std::string& position) override;
    void hide_sprite(const std::string& tag) override;
    void on_scene_changed(const std::string& room_id) override;
    void play_music(const std::string& path, int fadein_ms = 0,
                    bool noloop = false, double volume = -1.0) override;
    void stop_music(int fadeout_ms = 0) override;
    void play_sound(const std::string& path, bool loop = false) override;
    void stop_sound() override;

    MenuAction show_main_menu() override;
    void show_settings(GameSettings& settings) override;
    PauseAction show_pause_menu() override;
    void apply_settings(const GameSettings& settings) override;

private:
    void render_frame();
    void render_background();
    void render_sprites();
    void render_textbox(const std::string& speaker, const std::string& text);
    void render_choices(const std::vector<std::string>& options, int highlight);
    SDL_Texture* load_texture(const std::string& path);
    void wait_for_advance();
    std::string resolve_path(const std::string& relative) const;
    SDL_Rect text_wrap_render(const std::string& text, int x, int y, int max_width,
                              SDL_Color color);

    struct Button {
        SDL_Rect rect;
        std::string label;
        bool hovered = false;
    };
    bool render_button(Button& btn, TTF_Font* font);
    void render_slider(int x, int y, int w, int value, bool active);
    void play_ui_sound(const std::string& name);
    TTF_Font* font_title_ = nullptr;

    int width_;
    int height_;
    std::string title_;
    std::string content_root_;

    SDL_Window* window_ = nullptr;
    SDL_Renderer* renderer_ = nullptr;
    TTF_Font* font_ = nullptr;
    TTF_Font* font_small_ = nullptr;

    SDL_Texture* background_ = nullptr;
    std::unordered_map<std::string, Sprite> sprites_;
    std::unordered_map<std::string, SDL_Texture*> texture_cache_;

    Mix_Music* current_music_ = nullptr;
    std::string current_music_path_;
    std::unordered_map<std::string, Mix_Chunk*> chunk_cache_;
    int music_volume_ = MIX_MAX_VOLUME;
    int sfx_volume_ = MIX_MAX_VOLUME;

    bool running_ = true;
};

} // namespace novel::platform

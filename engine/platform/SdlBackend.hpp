#pragma once

#include "engine/platform/IBackend.hpp"

#include <SDL.h>
#include <SDL_image.h>
#include <SDL_mixer.h>
#include <SDL_ttf.h>

#include <memory>
#include <string>
#include <unordered_map>
#include <vector>

namespace novel::platform {

// ─── RAII deleters for SDL resources ─────────────────────────────────────────

namespace sdl_raii {
struct TextureDeleter { void operator()(SDL_Texture* p) const { if (p) SDL_DestroyTexture(p); } };
struct ChunkDeleter   { void operator()(Mix_Chunk* p)   const { if (p) Mix_FreeChunk(p); } };
struct MusicDeleter   { void operator()(Mix_Music* p)   const { if (p) Mix_FreeMusic(p); } };

using TexturePtr = std::unique_ptr<SDL_Texture, TextureDeleter>;
using ChunkPtr   = std::unique_ptr<Mix_Chunk,   ChunkDeleter>;
using MusicPtr   = std::unique_ptr<Mix_Music,   MusicDeleter>;
} // namespace sdl_raii

// ─── Sprite (non-owning texture ref into cache) ─────────────────────────────

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

    FlowSignal say(const std::string& speaker, const std::string& text) override;
    ChoiceResult choose(const std::vector<std::string>& options) override;
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
    // ── Reference design resolution (all pixel literals target this) ─────
    static constexpr int kRefW = 1280;
    static constexpr int kRefH = 720;

    /// Scale a horizontal design-pixel value to the current resolution.
    int sx(int v) const { return v * width_ / kRefW; }
    /// Scale a vertical design-pixel value to the current resolution.
    int sy(int v) const { return v * height_ / kRefH; }

    // ── Choice layout (scales to current resolution) ─────────────────────
    struct ChoiceLayout {
        int item_h;
        int spacing;
        int item_w;
        int item_x;
        int start_y;

        ChoiceLayout(int screen_w, int screen_h, int count)
            : item_h(screen_h * 54 / kRefH),
              spacing(screen_h * 8 / kRefH),
              item_w(screen_w * 3 / 5),
              item_x((screen_w - item_w) / 2),
              start_y((screen_h - (count * (item_h + spacing) - spacing)) / 2) {}

        int item_y(int index) const { return start_y + index * (item_h + spacing); }
    };

    // ── Rendering helpers ────────────────────────────────────────────────
    void render_frame();
    void render_background();
    void render_sprites();
    void render_textbox(const std::string& speaker, const std::string& text);
    void render_choices(const std::vector<std::string>& options, int highlight);
    SDL_Texture* load_texture(const std::string& path);
    FlowSignal wait_for_advance();
    FlowSignal render_typewriter(const std::string& speaker, const std::string& text);
    std::string resolve_path(const std::string& relative) const;
    SDL_Rect text_wrap_render(const std::string& text, int x, int y, int max_width,
                              SDL_Color color);

    // ── UI helpers ───────────────────────────────────────────────────────
    struct Button {
        SDL_Rect rect;
        std::string label;
        bool hovered = false;
    };
    bool render_button(Button& btn, TTF_Font* font);
    void render_slider(int x, int y, int w, int value, bool active);
    void play_ui_sound(const std::string& name);
    bool reload_fonts();

    // ── Window / renderer / fonts (manual cleanup due to aliasing) ──────
    int width_;
    int height_;
    std::string title_;
    std::string content_root_;

    SDL_Window* window_ = nullptr;
    SDL_Renderer* renderer_ = nullptr;
    TTF_Font* font_ = nullptr;
    TTF_Font* font_small_ = nullptr;
    TTF_Font* font_title_ = nullptr;

    // ── RAII-managed caches ──────────────────────────────────────────────
    SDL_Texture* background_ = nullptr;
    std::unordered_map<std::string, Sprite> sprites_;
    std::unordered_map<std::string, sdl_raii::TexturePtr> texture_cache_;

    sdl_raii::MusicPtr current_music_;
    std::string current_music_path_;
    std::unordered_map<std::string, sdl_raii::ChunkPtr> chunk_cache_;

    // ── Settings / state ─────────────────────────────────────────────────
    int music_volume_ = MIX_MAX_VOLUME;
    int sfx_volume_ = MIX_MAX_VOLUME;
    int text_speed_ = 50;
    bool running_ = true;
    bool shutdown_done_ = false;
};

} // namespace novel::platform

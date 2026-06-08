#pragma once

#include "engine/platform/IBackend.hpp"

namespace novel::platform {

/// Terminal-based backend (fallback when no GUI available).
class ConsoleBackend final : public IBackend {
public:
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
};

} // namespace novel::platform

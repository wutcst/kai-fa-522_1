#pragma once

#include "engine/platform/IBackend.hpp"

namespace novel::platform {

/// Terminal-based backend (fallback when no GUI available).
class ConsoleBackend final : public IBackend {
public:
    bool init() override;
    void shutdown() override;
    void say(const std::string& speaker, const std::string& text) override;
    int choose(const std::vector<std::string>& options) override;
    void show_background(const std::string& image_path) override;
    void show_sprite(const std::string& tag, const std::string& image_path,
                     const std::string& position) override;
    void hide_sprite(const std::string& tag) override;
    void on_scene_changed(const std::string& room_id) override;
    void play_music(const std::string& path) override;
    void stop_music() override;
    void play_sound(const std::string& path) override;
};

} // namespace novel::platform

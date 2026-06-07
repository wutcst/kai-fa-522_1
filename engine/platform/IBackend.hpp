#pragma once

#include <string>
#include <vector>

namespace novel::platform {

/// Abstract presentation layer for the visual novel engine.
class IBackend {
public:
    virtual ~IBackend() = default;

    virtual bool init() = 0;
    virtual void shutdown() = 0;

    /// Display narrative text (dialogue/narration). Blocks until player advances.
    virtual void say(const std::string& speaker, const std::string& text) = 0;

    /// Legacy overload for narration without speaker.
    void say(const std::string& text) { say("", text); }

    /// Present choices and return 0-based selection index.
    virtual int choose(const std::vector<std::string>& options) = 0;

    /// Set background image for current scene.
    virtual void show_background(const std::string& image_path) = 0;

    /// Show a character sprite at a position (left/center/right).
    virtual void show_sprite(const std::string& tag, const std::string& image_path,
                             const std::string& position) = 0;

    /// Hide a character sprite by tag.
    virtual void hide_sprite(const std::string& tag) = 0;

    /// Called when scene/room changes.
    virtual void on_scene_changed(const std::string& room_id) = 0;

    /// Play background music (looping).
    virtual void play_music(const std::string& path) = 0;

    /// Stop background music.
    virtual void stop_music() = 0;

    /// Play a sound effect (one-shot).
    virtual void play_sound(const std::string& path) = 0;
};

} // namespace novel::platform

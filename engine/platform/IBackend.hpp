#pragma once

#include "engine/platform/GameUI.hpp"

#include <string>
#include <vector>

namespace novel::platform {

/// Abstract presentation layer for the visual novel engine.
class IBackend {
public:
    virtual ~IBackend() = default;

    virtual bool init() = 0;
    virtual void shutdown() = 0;

    /// Show main menu and return selected action. Blocks until user chooses.
    virtual MenuAction show_main_menu() = 0;

    /// Show settings screen. Blocks until user closes it.
    virtual void show_settings(GameSettings& settings) = 0;

    /// Show pause menu (in-game). Blocks until user chooses.
    virtual PauseAction show_pause_menu() = 0;

    /// Apply current game settings to backend (volumes, fullscreen, etc.)
    virtual void apply_settings(const GameSettings& settings) = 0;

    /// Display narrative text (dialogue/narration). Blocks until player advances.
    /// Returns a flow signal indicating whether the user requested quit/main-menu.
    virtual FlowSignal say(const std::string& speaker, const std::string& text) = 0;

    /// Legacy overload for narration without speaker.
    FlowSignal say(const std::string& text) { return say("", text); }

    /// Present choices and return selection index + flow signal.
    virtual ChoiceResult choose(const std::vector<std::string>& options) = 0;

    /// Set background image for current scene.
    virtual void show_background(const std::string& image_path) = 0;

    /// Show a character sprite at a position (left/center/right).
    virtual void show_sprite(const std::string& tag, const std::string& image_path,
                             const std::string& position) = 0;

    /// Hide a character sprite by tag.
    virtual void hide_sprite(const std::string& tag) = 0;

    /// Called when scene/room changes.
    virtual void on_scene_changed(const std::string& room_id) = 0;

    /// Play background music. Loops unless noloop is true.
    /// fadein_ms: crossfade duration in milliseconds (0 = instant).
    /// volume: 0.0–1.0 (negative means keep current volume).
    virtual void play_music(const std::string& path, int fadein_ms = 0,
                            bool noloop = false, double volume = -1.0) = 0;

    /// Stop background music.
    /// fadeout_ms: fade-out duration in milliseconds (0 = immediate).
    virtual void stop_music(int fadeout_ms = 0) = 0;

    /// Play a sound effect. One-shot unless loop is true.
    virtual void play_sound(const std::string& path, bool loop = false) = 0;

    /// Stop all sound effect channels.
    virtual void stop_sound() = 0;

    /// Play looping ambient sound on a dedicated channel.
    virtual void play_ambient(const std::string& path) = 0;

    /// Stop the ambient sound channel.
    virtual void stop_ambient() = 0;

    /// Trigger a full-screen visual glitch effect for duration_ms.
    virtual void glitch(const std::string& type, int duration_ms = 300) = 0;

    /// Change the window title (SDL backend only).
    virtual void set_window_title(const std::string& title) = 0;

    /// Restore the default window title.
    virtual void reset_window_title() = 0;
};

} // namespace novel::platform

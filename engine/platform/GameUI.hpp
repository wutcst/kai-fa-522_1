#pragma once

#include "engine/core/Locale.hpp"

namespace novel::platform {

enum class FlowSignal {
    Continue,
    Quit,
    MainMenu,
    SaveRequest,
    LoadRequest,
};

enum class MenuAction {
    NewGame,
    Continue,
    Settings,
    Quit,
};

enum class PauseAction {
    Resume,
    Save,
    Load,
    Settings,
    MainMenu,
    Quit,
};

struct ChoiceResult {
    int selection = 0;
    FlowSignal signal = FlowSignal::Continue;
};

// ─── Resolution presets (16:9) ───────────────────────────────────────────────

struct Resolution {
    int width;
    int height;
};

inline constexpr Resolution kResolutions[] = {
    { 960,  540},
    {1280,  720},
    {1600,  900},
    {1920, 1080},
};
inline constexpr int kResolutionCount =
    static_cast<int>(sizeof(kResolutions) / sizeof(kResolutions[0]));
inline constexpr int kDefaultResolution = 1; // 1280x720

// ─── Settings ────────────────────────────────────────────────────────────────

struct GameSettings {
    int music_volume = 100;                        // 0–100
    int sfx_volume = 100;                          // 0–100
    int text_speed = 50;                           // 0–100 (0 = instant)
    int resolution_index = kDefaultResolution;     // index into kResolutions[]
    bool fullscreen = false;
    core::Language language = core::Language::English;
};

} // namespace novel::platform

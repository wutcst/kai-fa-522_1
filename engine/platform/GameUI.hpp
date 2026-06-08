#pragma once

namespace novel::platform {

enum class FlowSignal {
    Continue,
    Quit,
    MainMenu,
};

enum class MenuAction {
    NewGame,
    Settings,
    Quit,
};

enum class PauseAction {
    Resume,
    Settings,
    MainMenu,
    Quit,
};

struct ChoiceResult {
    int selection = 0;
    FlowSignal signal = FlowSignal::Continue;
};

struct GameSettings {
    int music_volume = 100;   // 0–100
    int sfx_volume = 100;     // 0–100
    int text_speed = 50;      // 0–100 (0 = instant)
    bool fullscreen = false;
};

} // namespace novel::platform

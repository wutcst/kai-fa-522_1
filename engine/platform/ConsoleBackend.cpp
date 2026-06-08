#include "engine/platform/ConsoleBackend.hpp"

#include <iostream>

namespace novel::platform {

bool ConsoleBackend::init() { return true; }
void ConsoleBackend::shutdown() {}

FlowSignal ConsoleBackend::say(const std::string& speaker, const std::string& text) {
    if (!speaker.empty()) {
        std::cout << speaker << ": " << text << '\n';
    } else {
        std::cout << text << '\n';
    }
    return FlowSignal::Continue;
}

ChoiceResult ConsoleBackend::choose(const std::vector<std::string>& options) {
    for (std::size_t i = 0; i < options.size(); ++i) {
        std::cout << (i + 1) << ". " << options[i] << '\n';
    }

    while (true) {
        std::cout << "> " << std::flush;
        std::string line;
        if (!std::getline(std::cin, line)) {
            return {static_cast<int>(options.size() - 1), FlowSignal::Continue};
        }

        try {
            const int choice = std::stoi(line);
            if (choice >= 1 && choice <= static_cast<int>(options.size())) {
                return {choice - 1, FlowSignal::Continue};
            }
        } catch (const std::invalid_argument&) {
        } catch (const std::out_of_range&) {
        }
        std::cout << "Please enter a number between 1 and " << options.size() << ".\n";
    }
}

void ConsoleBackend::show_background(const std::string& /*image_path*/) {}
void ConsoleBackend::show_sprite(const std::string& /*tag*/, const std::string& /*image_path*/,
                                  const std::string& /*position*/) {}
void ConsoleBackend::hide_sprite(const std::string& /*tag*/) {}
void ConsoleBackend::on_scene_changed(const std::string& /*room_id*/) {}
void ConsoleBackend::play_music(const std::string& /*path*/, int /*fadein_ms*/,
                                bool /*noloop*/, double /*volume*/) {}
void ConsoleBackend::stop_music(int /*fadeout_ms*/) {}
void ConsoleBackend::play_sound(const std::string& /*path*/, bool /*loop*/) {}
void ConsoleBackend::stop_sound() {}
void ConsoleBackend::play_ambient(const std::string& /*path*/) {}
void ConsoleBackend::stop_ambient() {}
void ConsoleBackend::glitch(const std::string& /*type*/, int /*duration_ms*/) {}
void ConsoleBackend::set_window_title(const std::string& /*title*/) {}
void ConsoleBackend::reset_window_title() {}
void ConsoleBackend::fake_crash(const std::string& message) {
    std::cout << "\n[FATAL ERROR] " << message << "\n";
}
int ConsoleBackend::show_slot_menu(bool saving, const std::vector<core::SaveSlotInfo>& slots) {
    std::cout << (saving ? "\nSave" : "\nLoad") << " — pick slot 1-" << slots.size() << " (0 cancel)\n> ";
    std::string line;
    std::getline(std::cin, line);
    try {
        const int pick = std::stoi(line);
        if (pick == 0) return -1;
        return pick - 1;
    } catch (...) {
        return -1;
    }
}
std::string ConsoleBackend::current_background() const { return {}; }
std::vector<core::GameSaveState::SpriteState> ConsoleBackend::current_sprites() const { return {}; }
void ConsoleBackend::clear_sprites() {}

MenuAction ConsoleBackend::show_main_menu(bool has_save, int /*playthrough_count*/, int /*launch_count*/) {
    std::cout << "\n=== DOKI DOKI LITERATURE CLUB: AFTER STORY ===\n";
    if (has_save) std::cout << "1. Continue\n";
    std::cout << (has_save ? "2. New Game\n3. Settings\n4. Quit\n> " : "1. New Game\n2. Settings\n3. Quit\n> ")
              << std::flush;
    std::string line;
    std::getline(std::cin, line);
    if (has_save) {
        if (line == "4") return MenuAction::Quit;
        if (line == "3") return MenuAction::Settings;
        if (line == "2") return MenuAction::NewGame;
        return MenuAction::Continue;
    }
    if (line == "3") return MenuAction::Quit;
    if (line == "2") return MenuAction::Settings;
    return MenuAction::NewGame;
}

void ConsoleBackend::show_settings(GameSettings& /*settings*/) {
    std::cout << "[Settings not available in console mode]\n";
}

PauseAction ConsoleBackend::show_pause_menu() {
    std::cout << "\n--- PAUSED ---\n1. Resume\n2. Save\n3. Load\n4. Settings\n5. Main Menu\n> " << std::flush;
    std::string line;
    std::getline(std::cin, line);
    if (line == "5") return PauseAction::MainMenu;
    if (line == "4") return PauseAction::Settings;
    if (line == "3") return PauseAction::Load;
    if (line == "2") return PauseAction::Save;
    return PauseAction::Resume;
}

void ConsoleBackend::apply_settings(const GameSettings& /*settings*/) {}

} // namespace novel::platform

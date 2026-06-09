#include "engine/Engine.hpp"
#include "engine/core/Locale.hpp"
#include "engine/core/PersistentStore.hpp"
#include "engine/platform/ConsoleBackend.hpp"
#include "engine/platform/GameUI.hpp"
#include "engine/platform/Paths.hpp"
#include "engine/platform/SdlBackend.hpp"

#include <filesystem>
#include <iostream>
#include <stdexcept>
#include <string>

namespace {

int pick_continue_slot(novel::platform::IBackend& backend, novel::Engine& engine) {
    const auto slots = engine.saves().list_slots();
    return backend.show_slot_menu(false, slots);
}

} // namespace

int main(int argc, char* argv[]) {
    bool use_console = false;
    for (int i = 1; i < argc; ++i) {
        if (std::string(argv[i]) == "--console") {
            use_console = true;
        }
    }

    const auto exe_dir = novel::platform::exe_directory();
    std::error_code ec;
    std::filesystem::current_path(exe_dir, ec);

    const std::filesystem::path game_root = ".";
    const std::filesystem::path content_root = "content";

    if (!std::filesystem::exists(content_root)) {
        std::cerr << "Content directory not found: content/\n";
        std::cerr << "Expected layout: <exe>/content/\n";
        return 1;
    }

    std::unique_ptr<novel::platform::IBackend> backend;
    if (use_console) {
        backend = std::make_unique<novel::platform::ConsoleBackend>();
    } else {
        auto& res = novel::platform::kResolutions[novel::platform::kDefaultResolution];
        backend = std::make_unique<novel::platform::SdlBackend>(
            res.width, res.height,
            "Doki Doki Literature Club: After Story",
            "content");
    }

    if (!backend->init()) {
        std::cerr << "Failed to initialize backend, falling back to console.\n";
        backend = std::make_unique<novel::platform::ConsoleBackend>();
        backend->init();
    }

    auto& locale = novel::core::Locale::instance();
    locale.set_language(novel::core::Language::English);
    locale.load_strings(content_root / "locale" / "en.json");

    novel::core::PersistentStore persistent(game_root);
    persistent.on_launch();

    novel::platform::GameSettings settings;

    try {
        while (true) {
            novel::Engine engine(*backend, game_root, content_root, persistent);
            const auto script_dir =
                content_root / "scripts" / novel::core::Locale::instance().script_subdir();
            engine.load_script_directory(script_dir);

            const auto action = backend->show_main_menu(
                engine.has_save(), persistent.playthrough_count(), persistent.launch_count());

            if (action == novel::platform::MenuAction::Quit) {
                break;
            }

            if (action == novel::platform::MenuAction::Settings) {
                backend->show_settings(settings);
                backend->apply_settings(settings);
                continue;
            }

            novel::platform::FlowSignal signal = novel::platform::FlowSignal::Continue;

            if (action == novel::platform::MenuAction::Continue) {
                const int slot = pick_continue_slot(*backend, engine);
                if (slot < 0) {
                    continue;
                }
                signal = engine.run_from_slot(slot);
            } else {
                engine.prepare_new_game();
                signal = engine.run("start");
            }

            if (signal == novel::platform::FlowSignal::Quit) {
                break;
            }
            if (signal == novel::platform::FlowSignal::MainMenu) {
                backend->stop_music(0);
                backend->stop_sound();
                backend->stop_ambient();
                backend->clear_sprites();
                backend->show_background("");
                backend->reset_window_title();
                continue;
            }
            break;
        }
    } catch (const std::runtime_error& e) {
        std::cerr << "Error: " << e.what() << '\n';
        return 1;
    }

    return 0;
}

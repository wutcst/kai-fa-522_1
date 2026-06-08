#include "engine/Engine.hpp"
#include "engine/platform/ConsoleBackend.hpp"
#include "engine/platform/GameUI.hpp"
#include "engine/platform/SdlBackend.hpp"

#include <filesystem>
#include <iostream>
#include <stdexcept>
#include <string>

namespace {

std::filesystem::path find_content_root() {
    std::filesystem::path candidate = "content";
    if (std::filesystem::exists(candidate)) return candidate;
    candidate = "../content";
    if (std::filesystem::exists(candidate)) return candidate;
    candidate = "../../content";
    if (std::filesystem::exists(candidate)) return candidate;
    return "content";
}

std::string content_file(const std::filesystem::path& root, const std::string& relative) {
    return (root / relative).string();
}

} // namespace

int main(int argc, char* argv[]) {
    bool use_console = false;
    for (int i = 1; i < argc; ++i) {
        if (std::string(argv[i]) == "--console") {
            use_console = true;
        }
    }

    const auto content_root = find_content_root();

    std::unique_ptr<novel::platform::IBackend> backend;
    if (use_console) {
        backend = std::make_unique<novel::platform::ConsoleBackend>();
    } else {
        backend = std::make_unique<novel::platform::SdlBackend>(
            1280, 720, "Doki Doki Literature Club: After Story", content_root.string());
    }

    if (!backend->init()) {
        std::cerr << "Failed to initialize backend, falling back to console.\n";
        backend = std::make_unique<novel::platform::ConsoleBackend>();
        backend->init();
    }

    novel::platform::GameSettings settings;

    try {
        while (true) {
            auto action = backend->show_main_menu();

            if (action == novel::platform::MenuAction::Quit) {
                break;
            }

            if (action == novel::platform::MenuAction::Settings) {
                backend->show_settings(settings);
                backend->apply_settings(settings);
                continue;
            }

            novel::Engine engine(*backend);
            engine.load_script_directory(content_file(content_root, "scripts"));

            auto signal = engine.run("start");

            if (signal == novel::platform::FlowSignal::Quit) {
                break;
            }
            if (signal == novel::platform::FlowSignal::MainMenu) {
                backend->stop_music(0);
                backend->stop_sound();
                continue;
            }
            break;
        }
    } catch (const std::runtime_error& e) {
        std::cerr << "Error: " << e.what() << '\n';
        backend->shutdown();
        return 1;
    }

    backend->shutdown();
    return 0;
}

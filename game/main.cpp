#include "engine/Engine.hpp"
#include "engine/platform/ConsoleBackend.hpp"
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

    try {
        const auto content_root = find_content_root();

        std::unique_ptr<novel::platform::IBackend> backend;
        if (use_console) {
            backend = std::make_unique<novel::platform::ConsoleBackend>();
        } else {
            backend = std::make_unique<novel::platform::SdlBackend>(
                1280, 720, "World of Zuul - Visual Novel", content_root.string());
        }

        if (!backend->init()) {
            std::cerr << "Failed to initialize backend, falling back to console.\n";
            backend = std::make_unique<novel::platform::ConsoleBackend>();
            backend->init();
        }

        novel::Engine engine(std::move(backend));

        engine.load_script_file(content_file(content_root, "scripts/world.rpy"));
        engine.load_script_file(content_file(content_root, "scripts/story.rpy"));
        engine.run("start");

    } catch (const std::runtime_error& e) {
        if (std::string(e.what()) == "quit") {
            return 0;
        }
        std::cerr << "Error: " << e.what() << '\n';
        return 1;
    }

    return 0;
}

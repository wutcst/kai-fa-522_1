#include "engine/Engine.hpp"
#include "engine/platform/ConsoleBackend.hpp"

#include <filesystem>
#include <iostream>
#include <stdexcept>

namespace {

std::filesystem::path content_path(const std::string& relative) {
    const std::filesystem::path beside_binary =
        std::filesystem::path("content") / relative;
    if (std::filesystem::exists(beside_binary)) {
        return beside_binary;
    }
    return std::filesystem::path("..") / "content" / relative;
}

} // namespace

int main() {
    try {
        novel::Engine engine(std::make_unique<novel::platform::ConsoleBackend>());

        engine.load_script_file(content_path("scripts/world.rpy").string());
        engine.load_script_file(content_path("scripts/story.rpy").string());
        engine.run("start");
    } catch (const std::exception& error) {
        std::cerr << "Error: " << error.what() << '\n';
        return 1;
    }

    return 0;
}

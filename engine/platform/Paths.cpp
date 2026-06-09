#include "engine/platform/Paths.hpp"

#include <SDL.h>

namespace novel::platform {

namespace {

bool ensure_sdl_init() {
    if (SDL_WasInit(0) != 0) {
        return true;
    }
    return SDL_Init(0) == 0;
}

std::filesystem::path normalize_dir(std::filesystem::path path) {
    if (path.empty()) {
        return ".";
    }
    if (path.filename().empty()) {
        path = path.parent_path();
    }
    return path.empty() ? std::filesystem::path(".") : path;
}

} // namespace

std::filesystem::path exe_directory() {
    if (!ensure_sdl_init()) {
        return ".";
    }

    char* base = SDL_GetBasePath();
    if (!base) {
        return ".";
    }

    const std::filesystem::path dir = normalize_dir(base);
    SDL_free(base);
    return dir;
}

std::filesystem::path content_directory() {
    return exe_directory() / "content";
}

std::string path_to_string(const std::filesystem::path& path) {
    return path.u8string();
}

} // namespace novel::platform

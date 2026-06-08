#pragma once

#include <filesystem>
#include <string>

namespace novel::platform {

/// Directory containing the running executable (no trailing separator).
std::filesystem::path exe_directory();

/// Read-only asset root: <exe>/content
std::filesystem::path content_directory();

std::string path_to_string(const std::filesystem::path& path);

} // namespace novel::platform

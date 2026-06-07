#pragma once

#include "engine/script/Ast.hpp"

#include <string>
#include <vector>

namespace novel::core {

/// Loads and parses Ren'Py-inspired script files from disk.
class ScriptLoader {
public:
    static script::ScriptModule load_file(const std::string& path);
    static script::ScriptModule load_source(const std::string& source, const std::string& name = "<script>");
    static script::ScriptModule merge(std::vector<script::ScriptModule> modules);
};

} // namespace novel::core

#include "engine/core/ScriptLoader.hpp"

#include "engine/script/Lexer.hpp"
#include "engine/script/Parser.hpp"

#include <fstream>
#include <sstream>
#include <stdexcept>
#include <unordered_set>

namespace novel::core {

script::ScriptModule ScriptLoader::load_file(const std::string& path) {
    std::ifstream input(path);
    if (!input) {
        throw std::runtime_error("failed to open script: " + path);
    }

    std::ostringstream buffer;
    buffer << input.rdbuf();
    return load_source(buffer.str(), path);
}

script::ScriptModule ScriptLoader::load_source(const std::string& source, const std::string& name) {
    try {
        script::Lexer lexer(source);
        script::Parser parser(lexer.tokens());
        return parser.parse();
    } catch (const std::exception& error) {
        throw std::runtime_error(name + ": " + error.what());
    }
}

script::ScriptModule ScriptLoader::merge(std::vector<script::ScriptModule> modules) {
    script::ScriptModule merged;
    std::unordered_set<std::string> room_ids;
    std::unordered_set<std::string> label_names;

    for (auto& module : modules) {
        for (auto& room : module.rooms) {
            if (!room_ids.insert(room.id).second) {
                throw std::runtime_error("duplicate room id: " + room.id);
            }
            merged.rooms.push_back(std::move(room));
        }
        for (auto& def : module.defaults) {
            merged.defaults.push_back(std::move(def));
        }
        for (auto& label : module.labels) {
            if (!label_names.insert(label.name).second) {
                throw std::runtime_error("duplicate label: " + label.name);
            }
            merged.labels.push_back(std::move(label));
        }
    }

    return merged;
}

} // namespace novel::core

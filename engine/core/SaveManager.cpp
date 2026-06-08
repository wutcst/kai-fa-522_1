#include "engine/core/SaveManager.hpp"

#include <chrono>
#include <fstream>
#include <iomanip>
#include <sstream>

namespace novel::core {

namespace {

std::string escape_string(const std::string& text) {
    std::string out;
    out.reserve(text.size() + 8);
    for (char ch : text) {
        switch (ch) {
        case '\\': out += "\\\\"; break;
        case '\n': out += "\\n"; break;
        case '\r': out += "\\r"; break;
        case '\t': out += "\\t"; break;
        default: out += ch; break;
        }
    }
    return out;
}

std::string unescape_string(const std::string& text) {
    std::string out;
    out.reserve(text.size());
    for (std::size_t i = 0; i < text.size(); ++i) {
        if (text[i] == '\\' && i + 1 < text.size()) {
            switch (text[i + 1]) {
            case 'n': out += '\n'; ++i; break;
            case 'r': out += '\r'; ++i; break;
            case 't': out += '\t'; ++i; break;
            case '\\': out += '\\'; ++i; break;
            default: out += text[i]; break;
            }
        } else {
            out += text[i];
        }
    }
    return out;
}

std::string value_to_line(const Value& value) {
    if (value.is_nil()) {
        return "null";
    }
    if (std::holds_alternative<bool>(value.data)) {
        return std::get<bool>(value.data) ? "true" : "false";
    }
    if (std::holds_alternative<double>(value.data)) {
        const double number = std::get<double>(value.data);
        if (number == static_cast<double>(static_cast<long long>(number))) {
            return std::to_string(static_cast<long long>(number));
        }
        std::ostringstream stream;
        stream << number;
        return stream.str();
    }
    return '"' + escape_string(std::get<std::string>(value.data)) + '"';
}

Value value_from_line(const std::string& line) {
    if (line == "null") {
        return Value::nil();
    }
    if (line == "true") {
        return Value::from_bool(true);
    }
    if (line == "false") {
        return Value::from_bool(false);
    }
    if (!line.empty() && line.front() == '"' && line.back() == '"') {
        return Value::from_string(unescape_string(line.substr(1, line.size() - 2)));
    }
    try {
        if (line.find('.') != std::string::npos) {
            return Value::from_number(std::stod(line));
        }
        return Value::from_number(static_cast<double>(std::stoll(line)));
    } catch (...) {
        return Value::from_string(line);
    }
}

} // namespace

SaveManager::SaveManager(std::filesystem::path game_root)
    : game_root_(std::move(game_root)), saves_dir_(game_root_ / "saves") {
    std::filesystem::create_directories(saves_dir_);
    std::filesystem::create_directories(characters_dir());
}

bool SaveManager::has_any_save() const {
    for (int slot = 0; slot < kSlotCount; ++slot) {
        if (std::filesystem::exists(slot_path(slot))) {
            return true;
        }
    }
    return false;
}

std::filesystem::path SaveManager::slot_path(int slot) const {
    return saves_dir_ / ("slot_" + std::to_string(slot) + ".sav");
}

std::filesystem::path SaveManager::slot_meta_path(int slot) const {
    return saves_dir_ / ("slot_" + std::to_string(slot) + "_monika.txt");
}

std::string SaveManager::format_timestamp() const {
    const auto now = std::chrono::system_clock::now();
    const auto time = std::chrono::system_clock::to_time_t(now);
    std::tm local_tm{};
#if defined(_WIN32)
    localtime_s(&local_tm, &time);
#else
    localtime_r(&time, &local_tm);
#endif
    std::ostringstream stream;
    stream << std::put_time(&local_tm, "%Y-%m-%d %H:%M");
    return stream.str();
}

bool SaveManager::save_slot(int slot, const GameSaveState& state) {
    if (slot < 0 || slot >= kSlotCount) {
        return false;
    }

    std::ofstream out(slot_path(slot));
    if (!out) {
        return false;
    }

    out << "version=1\n";
    out << "timestamp=" << format_timestamp() << '\n';
    out << "label=" << state.label << '\n';
    out << "statement_index=" << state.statement_index << '\n';
    out << "background=" << state.background << '\n';
    out << "save_generation=" << state.save_generation << '\n';
    out << "day=" << state.day << '\n';
    out << "glitch_count=" << state.glitch_count << '\n';
    out << "corrupted=" << (state.corrupted ? "true" : "false") << '\n';

    for (const auto& frame : state.return_stack) {
        out << "return=" << frame.label << ':' << frame.index << '\n';
    }
    for (const auto& sprite : state.sprites) {
        out << "sprite=" << sprite.tag << ':' << sprite.position << ':'
            << escape_string(sprite.path) << '\n';
    }
    for (const auto& [name, value] : state.variables) {
        out << "var." << name << '=' << value_to_line(value) << '\n';
    }

    if (state.corrupted || state.day >= 3 || state.glitch_count >= 2) {
        write_monika_meta(slot, state);
    }

    return true;
}

void SaveManager::write_monika_meta(int slot, const GameSaveState& state) const {
    std::ofstream meta(slot_meta_path(slot));
    if (!meta) {
        return;
    }

    meta << "SAVE FILE NOTICE\n";
    meta << "================\n\n";
    if (state.corrupted) {
        meta << "This save was touched while the world was unstable.\n";
        meta << "Loading it might not bring you back to where you think.\n\n";
    }
    meta << "Day " << state.day << " — " << state.label << '\n';
    meta << "Glitch count: " << state.glitch_count << "\n\n";
    meta << "I know you're trying to hold onto this moment.\n";
    meta << "But some moments weren't meant to be frozen.\n";
    meta << "Still... thank you for not giving up on us.\n\n";
    meta << "— Monika\n";
}

std::optional<GameSaveState> SaveManager::load_slot(int slot) const {
    const auto path = slot_path(slot);
    if (!std::filesystem::exists(path)) {
        return std::nullopt;
    }

    GameSaveState state;
    std::ifstream in(path);
    std::string line;
    while (std::getline(in, line)) {
        const auto pos = line.find('=');
        if (pos == std::string::npos) {
            continue;
        }
        const std::string key = line.substr(0, pos);
        const std::string value = line.substr(pos + 1);

        if (key == "label") {
            state.label = value;
        } else if (key == "statement_index") {
            state.statement_index = static_cast<std::size_t>(std::stoull(value));
        } else if (key == "background") {
            state.background = value;
        } else if (key == "save_generation") {
            state.save_generation = std::stoi(value);
        } else if (key == "day") {
            state.day = std::stoi(value);
        } else if (key == "glitch_count") {
            state.glitch_count = std::stoi(value);
        } else if (key == "corrupted") {
            state.corrupted = (value == "true");
        } else if (key == "return") {
            const auto colon = value.find(':');
            if (colon != std::string::npos) {
                ReturnFrame frame;
                frame.label = value.substr(0, colon);
                frame.index = static_cast<std::size_t>(std::stoull(value.substr(colon + 1)));
                state.return_stack.push_back(frame);
            }
        } else if (key == "sprite") {
            const auto first = value.find(':');
            const auto second = value.find(':', first + 1);
            if (first != std::string::npos && second != std::string::npos) {
                GameSaveState::SpriteState sprite;
                sprite.tag = value.substr(0, first);
                sprite.position = value.substr(first + 1, second - first - 1);
                sprite.path = unescape_string(value.substr(second + 1));
                state.sprites.push_back(std::move(sprite));
            }
        } else if (key.rfind("var.", 0) == 0) {
            state.variables[key.substr(4)] = value_from_line(value);
        }
    }

    if (state.label.empty()) {
        return std::nullopt;
    }
    return state;
}

void SaveManager::delete_slot(int slot) {
    std::error_code ec;
    std::filesystem::remove(slot_path(slot), ec);
    std::filesystem::remove(slot_meta_path(slot), ec);
}

std::vector<SaveSlotInfo> SaveManager::list_slots() const {
    std::vector<SaveSlotInfo> slots;
    slots.reserve(kSlotCount);

    for (int slot = 0; slot < kSlotCount; ++slot) {
        SaveSlotInfo info;
        info.slot = slot;
        if (auto state = load_slot(slot)) {
            info.exists = true;
            info.corrupted = state->corrupted || state->day >= 3 || state->glitch_count >= 2;
            info.day = state->day;
            info.label = state->label;
            info.summary = "Day " + std::to_string(state->day);
            if (info.corrupted) {
                info.summary = "??? Day " + std::to_string(state->day) + " ???";
            }

            std::ifstream in(slot_path(slot));
            std::string line;
            while (std::getline(in, line)) {
                if (line.rfind("timestamp=", 0) == 0) {
                    info.timestamp = line.substr(10);
                    break;
                }
            }

            if (std::filesystem::exists(slot_meta_path(slot))) {
                std::ifstream meta(slot_meta_path(slot));
                std::ostringstream note;
                note << meta.rdbuf();
                info.monika_note = note.str();
            }
        }
        slots.push_back(std::move(info));
    }
    return slots;
}

void SaveManager::restore_characters(const std::filesystem::path& content_root) const {
    const auto source = content_root / "characters";
    if (!std::filesystem::exists(source)) {
        return;
    }

    std::filesystem::create_directories(characters_dir());
    for (const auto& entry : std::filesystem::directory_iterator(source)) {
        if (!entry.is_regular_file()) {
            continue;
        }
        const auto target = characters_dir() / entry.path().filename();
        std::error_code ec;
        std::filesystem::copy_file(entry.path(), target,
                                   std::filesystem::copy_options::overwrite_existing, ec);
    }
}

bool SaveManager::character_exists(const std::string& name) const {
    return std::filesystem::exists(characters_dir() / (name + ".chr"));
}

bool SaveManager::delete_character(const std::string& name) const {
    std::error_code ec;
    return std::filesystem::remove(characters_dir() / (name + ".chr"), ec);
}

bool SaveManager::write_game_file(const std::string& relative_path,
                                  const std::string& content) const {
    const auto path = game_root_ / relative_path;
    std::filesystem::create_directories(path.parent_path());
    std::ofstream out(path);
    if (!out) {
        return false;
    }
    out << content;
    return true;
}

bool SaveManager::game_file_exists(const std::string& relative_path) const {
    return std::filesystem::exists(game_root_ / relative_path);
}

std::string SaveManager::read_game_file(const std::string& relative_path) const {
    std::ifstream in(game_root_ / relative_path);
    if (!in) {
        return {};
    }
    std::ostringstream stream;
    stream << in.rdbuf();
    return stream.str();
}

} // namespace novel::core

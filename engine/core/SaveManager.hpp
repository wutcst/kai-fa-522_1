#pragma once

#include "engine/core/Context.hpp"
#include "engine/core/Value.hpp"

#include <filesystem>
#include <optional>
#include <string>
#include <unordered_map>
#include <vector>

namespace novel::core {

struct ReturnFrame {
    std::string label;
    std::size_t index = 0;
};

struct SaveSlotInfo {
    int slot = 0;
    bool exists = false;
    bool corrupted = false;
    int day = 0;
    std::string label;
    std::string timestamp;
    std::string summary;
    std::string monika_note;
};

struct GameSaveState {
    std::string label;
    std::size_t statement_index = 0;
    std::vector<ReturnFrame> return_stack;
    std::unordered_map<std::string, Value> variables;
    std::string background;
    struct SpriteState {
        std::string tag;
        std::string path;
        std::string position = "center";
    };
    std::vector<SpriteState> sprites;
    int save_generation = 0;
    int day = 0;
    int glitch_count = 0;
    bool corrupted = false;
};

/// Save/load game state and meta-game save manipulation.
class SaveManager {
public:
    static constexpr int kSlotCount = 4;

    explicit SaveManager(std::filesystem::path game_root);

    bool has_any_save() const;
    std::vector<SaveSlotInfo> list_slots() const;

    bool save_slot(int slot, const GameSaveState& state);
    std::optional<GameSaveState> load_slot(int slot) const;
    void delete_slot(int slot);

    void restore_characters(const std::filesystem::path& content_root) const;
    bool character_exists(const std::string& name) const;
    bool delete_character(const std::string& name) const;
    bool write_game_file(const std::string& relative_path, const std::string& content) const;
    bool game_file_exists(const std::string& relative_path) const;
    std::string read_game_file(const std::string& relative_path) const;

    std::filesystem::path characters_dir() const { return game_root_ / "characters"; }
    std::filesystem::path game_root() const { return game_root_; }

private:
    std::filesystem::path slot_path(int slot) const;
    std::filesystem::path slot_meta_path(int slot) const;
    void write_monika_meta(int slot, const GameSaveState& state) const;
    std::string format_timestamp() const;

    std::filesystem::path game_root_;
    std::filesystem::path saves_dir_;
};

} // namespace novel::core

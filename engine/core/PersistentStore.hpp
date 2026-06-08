#pragma once

#include <cstdint>
#include <filesystem>
#include <string>

namespace novel::core {

/// Cross-playthrough persistent data (launch count, completions, play time).
class PersistentStore {
public:
    explicit PersistentStore(std::filesystem::path game_root);

    void on_launch();
    void on_game_completed();
    void add_play_seconds(std::uint64_t seconds);

    int playthrough_count() const { return playthrough_count_; }
    int launch_count() const { return launch_count_; }
    std::uint64_t total_play_seconds() const { return total_play_seconds_; }

    void save() const;

private:
    void load();

    std::filesystem::path path_;
    int playthrough_count_ = 0;
    int launch_count_ = 0;
    std::uint64_t total_play_seconds_ = 0;
};

} // namespace novel::core

#include "engine/core/PersistentStore.hpp"

#include <fstream>
#include <sstream>

namespace novel::core {

namespace {

std::string trim(const std::string& text) {
    const auto start = text.find_first_not_of(" \t\r\n");
    if (start == std::string::npos) {
        return {};
    }
    const auto end = text.find_last_not_of(" \t\r\n");
    return text.substr(start, end - start + 1);
}

} // namespace

PersistentStore::PersistentStore(std::filesystem::path game_root)
    : path_(std::move(game_root) / "persistent.dat") {
    load();
}

void PersistentStore::load() {
    if (!std::filesystem::exists(path_)) {
        return;
    }

    std::ifstream in(path_);
    std::string line;
    while (std::getline(in, line)) {
        const auto pos = line.find('=');
        if (pos == std::string::npos) {
            continue;
        }
        const std::string key = trim(line.substr(0, pos));
        const std::string value = trim(line.substr(pos + 1));
        if (key == "playthrough_count") {
            playthrough_count_ = std::stoi(value);
        } else if (key == "launch_count") {
            launch_count_ = std::stoi(value);
        } else if (key == "total_play_seconds") {
            total_play_seconds_ = static_cast<std::uint64_t>(std::stoull(value));
        }
    }
}

void PersistentStore::save() const {
    std::filesystem::create_directories(path_.parent_path());
    std::ofstream out(path_);
    out << "playthrough_count=" << playthrough_count_ << '\n';
    out << "launch_count=" << launch_count_ << '\n';
    out << "total_play_seconds=" << total_play_seconds_ << '\n';
}

void PersistentStore::on_launch() {
    ++launch_count_;
    save();
}

void PersistentStore::on_game_completed() {
    ++playthrough_count_;
    save();
}

void PersistentStore::add_play_seconds(std::uint64_t seconds) {
    total_play_seconds_ += seconds;
    save();
}

} // namespace novel::core

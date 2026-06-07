#include "engine/adventure/Room.hpp"

#include <algorithm>

namespace novel::adventure {

Room::Room(std::string id) : id_(std::move(id)) {}

void Room::set_description(std::string description) {
    description_ = std::move(description);
}

void Room::set_exit(const std::string& direction, const std::string& target_room) {
    exits_[direction] = target_room;
}

std::vector<std::string> Room::exit_directions() const {
    std::vector<std::string> directions;
    directions.reserve(exits_.size());
    for (const auto& [direction, _] : exits_) {
        directions.push_back(direction);
    }
    std::sort(directions.begin(), directions.end());
    return directions;
}

std::string Room::exit_target(const std::string& direction) const {
    const auto it = exits_.find(direction);
    if (it == exits_.end()) {
        return {};
    }
    return it->second;
}

bool Room::has_exit(const std::string& direction) const {
    return exits_.find(direction) != exits_.end();
}

} // namespace novel::adventure

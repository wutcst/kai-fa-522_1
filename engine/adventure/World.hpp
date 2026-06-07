#pragma once

#include "engine/adventure/Room.hpp"

#include <optional>
#include <string>
#include <unordered_map>

namespace novel::adventure {

/// Registry of all rooms and world-level queries.
class World {
public:
    Room& define_room(const std::string& id);
    const Room* room(const std::string& id) const;
    bool has_room(const std::string& id) const;

    std::string format_exits(const std::string& room_id) const;
    std::string format_description(const std::string& room_id) const;

    const std::unordered_map<std::string, Room>& rooms() const { return rooms_; }
    void clear();

private:
    std::unordered_map<std::string, Room> rooms_;
};

} // namespace novel::adventure

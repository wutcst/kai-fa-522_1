#include "engine/adventure/Player.hpp"

#include "engine/adventure/World.hpp"

namespace novel::adventure {

Player::Player(std::string start_room) : current_room_(std::move(start_room)) {}

void Player::set_room(const std::string& room_id) {
    current_room_ = room_id;
}

bool Player::can_go(const World& world, const std::string& direction) const {
    const Room* room = world.room(current_room_);
    if (!room) {
        return false;
    }
    if (!room->has_exit(direction)) {
        return false;
    }
    return world.has_room(room->exit_target(direction));
}

bool Player::go(World& world, const std::string& direction) {
    if (!can_go(world, direction)) {
        return false;
    }

    const Room* room = world.room(current_room_);
    current_room_ = room->exit_target(direction);
    return true;
}

} // namespace novel::adventure

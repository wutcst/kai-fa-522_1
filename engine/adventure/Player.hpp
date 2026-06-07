#pragma once

#include <string>

namespace novel::adventure {

class World;

/// Player state for text adventures (location, inventory hooks for future GalGame).
class Player {
public:
    explicit Player(std::string start_room);

    const std::string& current_room() const { return current_room_; }
    void set_room(const std::string& room_id);
    bool can_go(const World& world, const std::string& direction) const;
    bool go(World& world, const std::string& direction);

private:
    std::string current_room_;
};

} // namespace novel::adventure

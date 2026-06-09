#include "engine/adventure/World.hpp"
#include "engine/core/Locale.hpp"

#include <sstream>
#include <stdexcept>

namespace novel::adventure {

void World::clear() { rooms_.clear(); }

Room& World::define_room(const std::string& id) {
    auto [it, inserted] = rooms_.emplace(id, Room{id});
    if (!inserted) {
        throw std::runtime_error("duplicate room id: " + id);
    }
    return it->second;
}

const Room* World::room(const std::string& id) const {
    const auto it = rooms_.find(id);
    if (it == rooms_.end()) {
        return nullptr;
    }
    return &it->second;
}

bool World::has_room(const std::string& id) const {
    return rooms_.find(id) != rooms_.end();
}

std::string World::format_exits(const std::string& room_id) const {
    const Room* current = room(room_id);
    if (!current) {
        return {};
    }

    const auto directions = current->exit_directions();
    std::ostringstream stream;
    for (std::size_t i = 0; i < directions.size(); ++i) {
        if (i > 0) {
            stream << ' ';
        }
        stream << directions[i];
    }
    return stream.str();
}

std::string World::format_description(const std::string& room_id) const {
    const Room* current = room(room_id);
    if (!current) {
        return {};
    }
    return core::tr("world.description_prefix") + current->description() + core::tr("world.description_suffix");
}

} // namespace novel::adventure

#pragma once

#include <string>
#include <unordered_map>
#include <vector>

namespace novel::adventure {

/// A location in the adventure world with exits to neighboring rooms.
class Room {
public:
    explicit Room(std::string id);

    const std::string& id() const { return id_; }
    const std::string& description() const { return description_; }

    void set_description(std::string description);
    void set_exit(const std::string& direction, const std::string& target_room);
    std::vector<std::string> exit_directions() const;
    std::string exit_target(const std::string& direction) const;
    bool has_exit(const std::string& direction) const;

private:
    std::string id_;
    std::string description_;
    std::unordered_map<std::string, std::string> exits_;
};

} // namespace novel::adventure

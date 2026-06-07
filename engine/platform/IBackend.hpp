#pragma once

#include <string>
#include <vector>

namespace novel::platform {

/// Abstract presentation layer (console today, graphical UI for future GalGame).
class IBackend {
public:
    virtual ~IBackend() = default;

    virtual void say(const std::string& text) = 0;
    virtual int choose(const std::vector<std::string>& options) = 0;
    virtual void on_scene_changed(const std::string& room_id) = 0;
};

} // namespace novel::platform

#pragma once

#include "engine/platform/IBackend.hpp"

namespace novel::platform {

/// Terminal-based backend for text adventures.
class ConsoleBackend final : public IBackend {
public:
    void say(const std::string& text) override;
    int choose(const std::vector<std::string>& options) override;
    void on_scene_changed(const std::string& room_id) override;
};

} // namespace novel::platform

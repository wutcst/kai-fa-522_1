#include "engine/platform/ConsoleBackend.hpp"

#include <iostream>

namespace novel::platform {

void ConsoleBackend::say(const std::string& text) {
    std::cout << text << '\n';
}

int ConsoleBackend::choose(const std::vector<std::string>& options) {
    for (std::size_t i = 0; i < options.size(); ++i) {
        std::cout << (i + 1) << ". " << options[i] << '\n';
    }

    while (true) {
        std::cout << "> " << std::flush;
        std::string line;
        if (!std::getline(std::cin, line)) {
            return static_cast<int>(options.size() - 1);
        }

        try {
            const int choice = std::stoi(line);
            if (choice >= 1 && choice <= static_cast<int>(options.size())) {
                return choice - 1;
            }
        } catch (...) {
        }
        std::cout << "Please enter a number between 1 and " << options.size() << ".\n";
    }
}

void ConsoleBackend::on_scene_changed(const std::string& /*room_id*/) {}

} // namespace novel::platform

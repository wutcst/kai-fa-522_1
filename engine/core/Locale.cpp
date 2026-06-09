#include "engine/core/Locale.hpp"

#include <fstream>
#include <iostream>
#include <sstream>

namespace novel::core {

namespace {

std::string trim(const std::string& s) {
    const auto start = s.find_first_not_of(" \t\r\n");
    if (start == std::string::npos) return {};
    const auto end = s.find_last_not_of(" \t\r\n");
    return s.substr(start, end - start + 1);
}

std::string unescape_json_string(const std::string& s) {
    std::string out;
    out.reserve(s.size());
    for (std::size_t i = 0; i < s.size(); ++i) {
        if (s[i] == '\\' && i + 1 < s.size()) {
            switch (s[i + 1]) {
            case '"':  out += '"';  ++i; break;
            case '\\': out += '\\'; ++i; break;
            case 'n':  out += '\n'; ++i; break;
            case 't':  out += '\t'; ++i; break;
            default:   out += s[i]; break;
            }
        } else {
            out += s[i];
        }
    }
    return out;
}

const std::string kEnglishName = "English";
const std::string kChineseName = "\xe4\xb8\xad\xe6\x96\x87";

} // namespace

Locale::Locale() = default;

Locale& Locale::instance() {
    static Locale inst;
    return inst;
}

void Locale::set_language(Language lang) {
    language_ = lang;
}

void Locale::toggle_language() {
    language_ = (language_ == Language::English) ? Language::Chinese : Language::English;
}

const std::string& Locale::language_name() const {
    return language_ == Language::English ? kEnglishName : kChineseName;
}

std::string Locale::script_subdir() const {
    switch (language_) {
    case Language::Chinese: return "zh";
    default:                return "en";
    }
}

const std::string& Locale::tr(const std::string& key) const {
    const auto it = strings_.find(key);
    if (it != strings_.end()) {
        return it->second;
    }
    return key;
}

void Locale::load_strings(const std::string& path) {
    strings_.clear();

    std::ifstream file(path);
    if (!file) {
        std::cerr << "Locale: failed to open " << path << '\n';
        return;
    }

    std::string line;
    while (std::getline(file, line)) {
        line = trim(line);
        if (line.empty() || line[0] == '{' || line[0] == '}' || line[0] == '/') {
            continue;
        }

        if (line.back() == ',') {
            line.pop_back();
        }

        const auto colon = line.find(':');
        if (colon == std::string::npos) continue;

        std::string raw_key = trim(line.substr(0, colon));
        std::string raw_val = trim(line.substr(colon + 1));

        if (raw_key.size() >= 2 && raw_key.front() == '"' && raw_key.back() == '"') {
            raw_key = raw_key.substr(1, raw_key.size() - 2);
        }
        if (raw_val.size() >= 2 && raw_val.front() == '"' && raw_val.back() == '"') {
            raw_val = raw_val.substr(1, raw_val.size() - 2);
        }

        strings_[unescape_json_string(raw_key)] = unescape_json_string(raw_val);
    }
}

} // namespace novel::core

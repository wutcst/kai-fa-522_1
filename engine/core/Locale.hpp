#pragma once

#include <string>
#include <unordered_map>

namespace novel::core {

enum class Language { English, Chinese };

class Locale {
public:
    static Locale& instance();

    void set_language(Language lang);
    Language language() const { return language_; }

    /// Toggle to the next language in the cycle.
    void toggle_language();

    /// Look up a translated string by key.  Returns the key itself if no
    /// translation is found, so untranslated keys are still visible.
    const std::string& tr(const std::string& key) const;

    /// Human-readable name for the current language (in its own language).
    const std::string& language_name() const;

    /// Subdirectory name under content/scripts/ for the current language.
    std::string script_subdir() const;

    /// Load string table from a JSON file (simplified key-value format).
    void load_strings(const std::string& path);

private:
    Locale();

    Language language_ = Language::English;
    std::unordered_map<std::string, std::string> strings_;
};

/// Global shorthand for Locale::instance().tr(key).
inline const std::string& tr(const std::string& key) {
    return Locale::instance().tr(key);
}

} // namespace novel::core

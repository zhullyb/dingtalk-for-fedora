// LD_PRELOAD hook: keep plain-text newlines when pasting into DingTalk's
// native rich input. The client treats clipboard text as Markdown
// (enable_native_input_paste_markdown_1013), and CommonMark collapses a
// single "\n" into a space. Force the vendor rollback + disable that gray
// switch so paste uses HandleInsertTextFromMimeData instead.
#include <dlfcn.h>

#include <string>

namespace {

bool override_gray(const std::string& module, const std::string& key, bool* out) {
    if (module != "im") {
        return false;
    }
    if (key == "rollback_paste_match_plain_text_markdown") {
        if (out) {
            *out = true;
        }
        return true;
    }
    if (key == "enable_native_input_paste_markdown" ||
        key == "enable_native_input_paste_markdown_1013" ||
        key == "enable_native_input_paste_markdown_linux") {
        if (out) {
            *out = false;
        }
        return true;
    }
    return false;
}

template <typename Fn>
Fn orig(const char* name) {
    static Fn fn;
    static bool inited;
    if (!inited) {
        fn = reinterpret_cast<Fn>(dlsym(RTLD_NEXT, name));
        inited = true;
    }
    return fn;
}

}  // namespace

using GetGray4 = bool (*)(void*, const std::string&, const std::string&, bool, bool*);
using GetGrayOrg = bool (*)(void*, const std::string&, const std::string&, bool, long, bool*);

extern "C" bool _ZN4gaea6config13ConfigService13GetGraySwitchERKNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEEES9_bPb(
    void* self, const std::string& module, const std::string& key, bool def, bool* found) {
    bool forced = false;
    if (override_gray(module, key, &forced)) {
        if (found) {
            *found = true;
        }
        return forced;
    }
    auto fn = orig<GetGray4>(
        "_ZN4gaea6config13ConfigService13GetGraySwitchERKNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEEES9_bPb");
    return fn ? fn(self, module, key, def, found) : def;
}

extern "C" bool _ZN4gaea6config13ConfigService22GetGraySwitchWithOrgIdERKNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEEES9_blPb(
    void* self, const std::string& module, const std::string& key, bool def, long org,
    bool* found) {
    bool forced = false;
    if (override_gray(module, key, &forced)) {
        if (found) {
            *found = true;
        }
        return forced;
    }
    auto fn = orig<GetGrayOrg>(
        "_ZN4gaea6config13ConfigService22GetGraySwitchWithOrgIdERKNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEEES9_blPb");
    return fn ? fn(self, module, key, def, org, found) : def;
}

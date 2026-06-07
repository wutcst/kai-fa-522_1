add_library(novel_engine
    adventure/Player.cpp
    adventure/Room.cpp
    adventure/World.cpp
    core/Context.cpp
    core/ScriptLoader.cpp
    core/Value.cpp
    Engine.cpp
    narrative/BuiltinApi.cpp
    narrative/Executor.cpp
    narrative/ExpressionEvaluator.cpp
    platform/ConsoleBackend.cpp
    platform/SdlBackend.cpp
    platform/SdlMenuUI.cpp
    script/Lexer.cpp
    script/Parser.cpp
)

add_library(novel::engine ALIAS novel_engine)

target_include_directories(novel_engine
    PUBLIC
        ${CMAKE_CURRENT_SOURCE_DIR}/..
)

target_compile_features(novel_engine PUBLIC cxx_std_17)

target_link_libraries(novel_engine
    PUBLIC
        SDL2::SDL2-static
        SDL2_image::SDL2_image-static
        SDL2_ttf::SDL2_ttf-static
        SDL2_mixer::SDL2_mixer-static
)

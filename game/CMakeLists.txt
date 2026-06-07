add_executable(zuul main.cpp)

target_link_libraries(zuul PRIVATE novel::engine)

if(WIN32)
    target_link_libraries(zuul PRIVATE SDL2::SDL2main)
endif()

add_custom_command(TARGET zuul POST_BUILD
    COMMAND ${CMAKE_COMMAND} -E copy_directory
        ${CMAKE_SOURCE_DIR}/content
        $<TARGET_FILE_DIR:zuul>/content
    COMMENT "Copying game content next to executable"
)

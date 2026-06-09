add_executable(ddlc_afterstory main.cpp)

target_link_libraries(ddlc_afterstory PRIVATE novel::engine)

if(WIN32)
    target_link_libraries(ddlc_afterstory PRIVATE SDL2::SDL2main)
    set_target_properties(ddlc_afterstory PROPERTIES
        WIN32_EXECUTABLE $<IF:$<CONFIG:Debug>,FALSE,TRUE>
    )
endif()

add_custom_target(copy_content ALL
    COMMAND ${CMAKE_COMMAND} -E copy_directory
        ${CMAKE_SOURCE_DIR}/content
        $<TARGET_FILE_DIR:ddlc_afterstory>/content
    COMMENT "Copying game content next to executable"
)
add_dependencies(copy_content ddlc_afterstory)

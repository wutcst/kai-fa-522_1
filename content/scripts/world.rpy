# AfterStory - World Definition
# A continuation after the "good ending" of Doki Doki Literature Club

room residential:
    description "on the quiet residential street leading to school"
    exit east school_corridor

room school_corridor:
    description "in the school corridor, the afternoon sun casting long shadows"
    exit west residential
    exit north classroom
    exit east clubroom

room classroom:
    description "in your usual classroom, desks neatly arranged"
    exit south school_corridor

room clubroom:
    description "in the Literature Club room, a few desks pushed together"
    exit west school_corridor

room sayori_house:
    description "outside Sayori's house, the familiar door before you"
    exit south residential

room mc_bedroom:
    description "in your bedroom, everything exactly where you left it"
    exit south residential

# Game state variables
default start_room = "clubroom"
default player_name = "Player"

default day = 1
default act = 1

default sayori_affection = 0
default natsuki_affection = 0
default yuri_affection = 0
default monika_affection = 0

default poem_written = false
default noticed_glitch = false
default heard_static = false
default saw_monika_shadow = false
default desk_note_found = false
default sayori_overslept = false
default strange_poem_read = false

default glitch_count = 0
default reality_cracks = 0

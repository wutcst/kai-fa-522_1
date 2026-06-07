# World Definition - Hoshimi Academy

room outside:
    description "at the front gate of Hoshimi Academy"
    exit east theater
    exit south lab
    exit west pub

room theater:
    description "in the large lecture hall"
    exit west outside

room pub:
    description "inside Cafe Plume, the cozy cafe near campus"
    exit east outside

room lab:
    description "in the computer room"
    exit north outside
    exit east office

room office:
    description "in the Student Council room"
    exit west lab

default start_room = "outside"

# Story progress
default day = 1
default chapter = 1

# Affection counters
default kaede_affection = 0
default ruru_affection = 0
default kotori_affection = 0

# Scene visit flags
default visited_theater = false
default visited_pub = false
default visited_lab = false
default visited_office = false

# Character encounter flags
default met_kaede = false
default met_ruru = false
default met_kotori = false

# Event flags - Kaede route
default kaede_bento_event = false
default kaede_umbrella_event = false
default kaede_late_night_event = false
default kaede_festival_event = false

# Event flags - Ruru route
default ruru_bug_event = false
default ruru_lunch_event = false
default ruru_game_jam_event = false
default ruru_all_nighter_event = false

# Event flags - Kotori route
default kotori_lost_event = false
default kotori_poem_event = false
default kotori_rain_event = false
default kotori_closing_event = false

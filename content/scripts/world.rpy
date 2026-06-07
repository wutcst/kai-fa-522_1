# World definition - rooms and initial state

room outside:
    description "outside the main entrance of the university"
    exit east theater
    exit south lab
    exit west pub

room theater:
    description "in a lecture theater"
    exit west outside

room pub:
    description "in the campus pub"
    exit east outside

room lab:
    description "in a computing lab"
    exit north outside
    exit east office

room office:
    description "in the computing admin office"
    exit west lab

default start_room = "outside"
default visited_theater = false
default visited_lab = false
default visited_pub = false
default player_name = "Player"

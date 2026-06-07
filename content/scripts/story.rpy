# World of Zuul - Visual Novel Story Script

label start:
    scene outside
    bg "images/bg_outside.png"
    "Welcome to the World of Zuul!"
    "A mysterious university campus stretches before you."
    "The old stone buildings hold many secrets..."
    jump game_loop

label game_loop:
    call show_room
    menu:
        "Look around":
            call look_around
            jump game_loop
        "Travel":
            jump travel_menu
        "Talk":
            call try_talk
            jump game_loop
        "Quit":
            jump end_game

label show_room:
    "[room_description()]"
    "Exits: [room_exits()]"
    return

label look_around:
    if current_room() == "outside":
        "The main entrance towers above you, its gothic arches casting long shadows."
        "Students hurry past, clutching books and laptops."
    if current_room() == "theater":
        "Rows of seats rise steeply toward the back of the lecture hall."
        "A dusty projector sits on the desk, waiting for the next presentation."
    if current_room() == "pub":
        "The warm glow of amber lights fills the cozy pub."
        "Old photographs of university teams line the walls."
    if current_room() == "lab":
        "Monitors flicker with code and terminal windows."
        "The quiet hum of cooling fans fills the air."
    if current_room() == "office":
        "Filing cabinets line the walls, neatly labeled by year."
        "A half-finished cup of tea sits on the administrator's desk."
    return

label try_talk:
    if current_room() == "outside":
        show guide "images/char_guide.png" at center
        guide "Hey there! Welcome to the university."
        guide "I'm your campus guide. Feel free to explore!"
        guide "The theater is to the east, and the pub is west."
        hide guide
    elif current_room() == "theater":
        show professor "images/char_professor.png" at center
        professor "Ah, a student! Are you here for the lecture?"
        professor "I'm afraid class doesn't start until next week."
        hide professor
    elif current_room() == "pub":
        show barkeep "images/char_barkeep.png" at center
        barkeep "What'll it be? We've got tea, coffee, and..."
        barkeep "Well, this IS a university pub."
        hide barkeep
    elif current_room() == "lab":
        show student "images/char_student.png" at center
        student "Shh! I'm trying to debug this segfault."
        student "...it's been three days."
        hide student
    else:
        "There's no one here to talk to right now."
    return

label travel_menu:
    menu:
        "Go East":
            if can_go("east"):
                go east
                call on_enter_room
                jump game_loop
            else:
                "There's no path to the east."
                jump travel_menu
        "Go South":
            if can_go("south"):
                go south
                call on_enter_room
                jump game_loop
            else:
                "There's no path to the south."
                jump travel_menu
        "Go West":
            if can_go("west"):
                go west
                call on_enter_room
                jump game_loop
            else:
                "There's no path to the west."
                jump travel_menu
        "Go North":
            if can_go("north"):
                go north
                call on_enter_room
                jump game_loop
            else:
                "There's no path to the north."
                jump travel_menu
        "Stay here":
            jump game_loop

label on_enter_room:
    if current_room() == "outside":
        bg "images/bg_outside.png"
    if current_room() == "theater":
        bg "images/bg_theater.png"
        if not visited_theater:
            $ visited_theater = true
            "You step into the grand lecture theater for the first time."
            "The sheer size of it takes your breath away."
    if current_room() == "pub":
        bg "images/bg_pub.png"
        if not visited_pub:
            $ visited_pub = true
            "A wave of warmth and the smell of coffee greets you."
    if current_room() == "lab":
        bg "images/bg_lab.png"
        if not visited_lab:
            $ visited_lab = true
            "Rows of computers hum softly in the dim light."
            "The air smells of ozone and energy drinks."
    if current_room() == "office":
        bg "images/bg_office.png"
    return

label end_game:
    "Thank you for exploring the World of Zuul!"
    "Perhaps next time you'll uncover more of its secrets..."
    return

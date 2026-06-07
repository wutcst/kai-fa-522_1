# Main story script (Ren'Py-inspired syntax)

label start:
    scene outside
    "Welcome to the World of Zuul!"
    "World of Zuul is a new, incredibly boring adventure game."
    "Type a number in menus to explore the university."
    jump game_loop

label game_loop:
    call show_room
    menu:
        "Look around":
            jump game_loop
        "Travel":
            jump travel_menu
        "Help":
            "You are lost. You are alone. You wander around at the university."
            "Use menus to move between rooms, or type the shown number."
            jump game_loop
        "Quit":
            jump end_game

label travel_menu:
    menu:
        "East":
            if can_go("east"):
                go east
                call on_enter_room
                jump game_loop
            else:
                "There is no door!"
                jump travel_menu
        "South":
            if can_go("south"):
                go south
                call on_enter_room
                jump game_loop
            else:
                "There is no door!"
                jump travel_menu
        "West":
            if can_go("west"):
                go west
                call on_enter_room
                jump game_loop
            else:
                "There is no door!"
                jump travel_menu
        "North":
            if can_go("north"):
                go north
                call on_enter_room
                jump game_loop
            else:
                "There is no door!"
                jump travel_menu
        "Back":
            jump game_loop

label show_room:
    "[room_description()]"
    "Exits: [room_exits()]"
    return

label on_enter_room:
    if current_room() == "theater" and not visited_theater:
        $ visited_theater = true
        "This is your first time in the lecture theater."
    if current_room() == "lab" and not visited_lab:
        $ visited_lab = true
        "The lab machines hum quietly as you enter."
    return

label end_game:
    "Thank you for playing.  Good bye."
    return

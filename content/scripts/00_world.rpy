# ============================================================
# WORLD DEFINITIONS
# Rooms, variables, and game state defaults
# ============================================================

room residential:
    description "A quiet suburban neighborhood lined with cherry blossom trees."
    exit north school_corridor
    exit east park

room school_corridor:
    description "A long hallway with rows of lockers and fluorescent lights."
    exit south residential
    exit east classroom
    exit north clubroom

room classroom:
    description "A standard classroom with rows of desks facing a blackboard."
    exit west school_corridor

room clubroom:
    description "The Literature Club room — desks arranged in a circle, bookshelves along the walls, afternoon sun through tall windows."
    exit south school_corridor

room park:
    description "A peaceful park with benches and a small fountain."
    exit west residential

room library:
    description "Tall shelves packed with books. The air smells of old paper."
    exit south school_corridor

# --- Game State Variables ---

default day = 0
default act = 1

default sayori_affection = 0
default natsuki_affection = 0
default yuri_affection = 0

default noticed_glitch = false
default desk_note_found = false
default saw_monika_shadow = false
default heard_static = false
default strange_poem_read = false
default poem_written = false
default sayori_overslept = false

default glitch_count = 0
default reality_cracks = 0

default playthrough = 0
default launch_count = 0
default save_generation = 0
default just_loaded = false
default monika_chr_deleted = false
default ending_reached = false
default ending_type = "normal"
default meta_file_written = false
default secret_file_written = false

# --- Meta hooks ---

label save_loaded_hook:
    if just_loaded:
        if day >= 3 or glitch_count >= 2:
            window title "You came back"
            "For a moment, the world stutters — like a tape rewinding."
            if glitch_count >= 2:
                "A thought that isn't mine flickers behind my eyes:"
                "'So you wanted to go back. I understand.'"
            window title reset
    return

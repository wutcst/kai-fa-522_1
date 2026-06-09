# ============================================================
# DOKI DOKI LITERATURE CLUB: AFTER STORY
# A DLC continuation - Sweet days with unsettling undertones
# ============================================================
# Setting: After the "good ending" of DDLC, where the player
# spent time with all club members. The world has been "reset"
# with Sayori as president. Everything seems perfect...
# but Monika's presence lingers in the gaps between moments.
# ============================================================

# === PROLOGUE ===

label start:
    bg "images/bg/bedroom.png"
    play music "audio/bgm/10.ogg"

    if get_playthrough() >= 2:
        window title "You came back"
        "Something about this morning feels... rehearsed."
        "Like I've lived this exact sunrise before."
        window title reset

    if get_launch_count() >= 3 and get_playthrough() >= 1:
        "Before I even sit up, a whisper of déjà vu curls at the edge of my mind."
        "As if someone is glad I returned."

    if get_hour() >= 0 and get_hour() < 4:
        "It's far too late — or far too early — to be waking up like this."
        "The room is quiet in a way that feels almost watchful."

    if not character_exists("monika"):
        $ monika_chr_deleted = true

    "..."

    "I open my eyes."

    "Sunlight streams through the curtains, painting golden stripes across the ceiling."

    "For a moment, I just lie here. Breathing. Existing."

    "There's a warmth in my chest — a feeling of contentment that I can't quite explain."

    "Like I've been given something precious."

    "A second chance, maybe."

    "I don't remember what came before this. There's a haze where my memories should be."

    "But that's fine."

    "Because right now, in this moment, everything is exactly as it should be."

    "..."

    "Today is a new day."

    "And I intend to make it a good one."

    stop music

    jump day1_morning

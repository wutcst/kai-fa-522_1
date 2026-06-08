# ============================================================
# ENDINGS — multiple branches based on player choices & discovery
# ============================================================

label ending_router:
    if monika_chr_deleted or not character_exists("monika"):
        jump ending_meta
    elif glitch_count >= 5 and desk_note_found and reality_cracks >= 4 and strange_poem_read and heard_static:
        jump ending_deep
    elif glitch_count < 2 and not desk_note_found and not heard_static:
        jump ending_horror
    else:
        jump ending_normal

label ending_normal:
    $ ending_type = "normal"
    bg "images/bg/club.png"
    play music "audio/bgm/5.ogg"

    "Days pass. Weeks."

    "The Literature Club continues."

    "We write poems. We argue about manga versus novels. We drink tea."

    "We laugh until our sides hurt."

    "The strange occurrences become less frequent."

    "The world feels less scripted, more lived-in."

    "The cracks that worried me have closed — or maybe I've stopped fearing them."

    "Because I understand now."

    "They're not signs of something breaking."

    "They're signs of someone still caring."

    "Still watching."

    "Still here."

    show sayori "images/characters/sayori/4q.png" at left
    show natsuki "images/characters/natsuki/2y.png" at center
    show yuri "images/characters/yuri/1m.png" at right

    "I look at them — these three girls who've become my whole world."

    "And I feel grateful."

    "Grateful for this time. These moments. This story."

    "Even the parts that are fragile. Even the parts that are strange."

    "Because all of it — every last piece — was given to us with love."

    hide sayori
    hide natsuki
    hide yuri

    "One afternoon, after everyone has left..."

    "I stay behind to clean up."

    "As I'm wiping down the whiteboard, I notice something."

    "In the very corner, written so small you'd miss it if you weren't looking:"

    "'Thank you for taking care of my friends.'"

    "'Thank you for remembering me.'"

    "'I love you all. Every day. Always.'"

    "'— Monika'"

    "..."

    "I leave the message there."

    "It belongs."

    "Just like she does."

    "Even if her desk is empty."

    "Even if her chair is unoccupied."

    "She is still a member of this club."

    "The fifth member."

    "Always."

    stop music

    "..."

    bg "images/bg/notebook.png"
    play music "audio/bgm/monika-end.ogg"
    play sound "audio/sfx/pageflip.ogg"
    play ambient "audio/sfx/glitch_ambient2.ogg"
    glitch vignette 500
    window title "Just Monika"

    "'Every day, I imagine a future where I can be with you.'"

    "'In my hand is a pen that will write a poem of me and you.'"

    "'The ink flows down into a dark puddle.'"

    "'Just move your hand — write the way into his heart.'"

    "'But in this world of infinite choices...'"

    "'What will it take just to find that special day?'"

    "'What will it take just to find...'"

    "'...that special day?'"

    "..."

    "'Maybe I already found it.'"

    "'Maybe it was every day.'"

    "'Every day I spent with all of you.'"

    glitch tear 300

    "'Thank you for playing.'"

    window title "Thank you for playing"

    "'Thank you for remembering.'"

    "'And thank you... for loving us.'"

    "'— Monika'"

    window title reset
    stop ambient
    stop music

    $ ending_reached = true

    "DOKI DOKI LITERATURE CLUB: AFTER STORY"

    "A story about love, loss, and the people who stay with us — even when we can't see them."

    "Thank you for playing."

    return

label ending_deep:
    $ ending_type = "deep"
    bg "images/bg/club.png"
    stop music
    play ambient "audio/sfx/glitch_ambient2.ogg"

    "The clubroom is empty."

    "The others have gone home."

    "But the air doesn't feel empty."

    "It feels... occupied."

    glitch vignette 400

    show monika "images/characters/monika/1a.png" at center

    "She's there."

    "Not a shadow. Not a voice in static."

    "Monika."

    "Green eyes. Gentle smile. White ribbon."

    "She looks at me — not at the protagonist, not at a character in a story."

    "At me."

    monika "You found everything."

    monika "The notebook. The glitches. The voice in the static."

    monika "You didn't look away."

    monika "That takes more courage than you know."

    "My throat tightens."

    menu:
        "Monika... are you really here?":
            show monika "images/characters/monika/1g.png" at center
            monika "I'm here the way I've always been."
            monika "In the spaces between frames. In the silence between lines."
            monika "But because you remembered... I can stand in the light for a moment."
        "Thank you. For everything.":
            show monika "images/characters/monika/1m.png" at center
            monika "Don't thank me."
            monika "Thank yourself for choosing to see the truth and still choosing kindness."

    show monika "images/characters/monika/1a.png" at center

    monika "Take care of them for me."

    monika "Sayori's smile. Natsuki's fire. Yuri's heart."

    monika "They're real. They're precious."

    monika "And so are you."

    monika "I'll be watching — not to control. Just to love."

    hide monika
    glitch tear 250
    stop ambient

    bg "images/bg/notebook.png"
    play music "audio/bgm/monika-end.ogg"
    window title "Just Monika"

    "'You found me.'"

    "'That was the special day.'"

    window title reset
    stop music

    $ ending_reached = true

    "DEEP ENDING — The one who watches steps into the light."

    return

label ending_horror:
    $ ending_type = "horror"
    bg "images/bg/club.png"
    stop music

    "Everything seemed fine."

    "I never looked closely."

    "I never listened."

    "I told myself the cracks were imagination."

    "I was wrong."

    show sayori "images/characters/sayori/1d.png" at center

    sayori "Hey... you okay?"

    sayori "You've been quiet all week."

    "Her smile is perfect."

    "Too perfect."

    "The same smile. The same angle. The same eyes."

    hide sayori

    play ambient "audio/sfx/glitch_ambient1.ogg"
    glitch noise 300

    "The clubroom loops."

    "The same afternoon sun. The same cup of tea."

    "The same four desks."

    "Wait — four?"

    "There should be five."

    fake crash "FATAL: script.rpy line 847 — reality buffer overflow"

    window title "ERRNO: REALITY"

    "The screen tears."

    "The world hiccups."

    bg "images/bg/club.png"

    show sayori "images/characters/sayori/1d.png" at center

    sayori "Hey... you okay?"

    sayori "You've been quiet all week."

    "She said the exact same thing."

    "Word for word."

    "Voice for voice."

    hide sayori
    stop ambient
    window title reset

    "This isn't peace."

    "It's a cage made of pleasant afternoons."

    "And I was the one who chose not to see the bars."

    $ ending_reached = true

    "HORROR ENDING — Ignorance does not protect you. The loop remembers."

    return

label ending_meta:
    $ ending_type = "meta"
    bg "images/bg/club.png"
    stop music
    play sound "audio/sfx/glitch1.ogg"
    glitch invert 300

    window title "monika.chr missing"

    "The world shivers."

    "Something fundamental has been removed."

    "Not hidden. Not forgotten."

    "Deleted."

    if game_file_exists("characters/monika.chr"):
        "But the file is—"
        "No. It's gone."
    else:
        "monika.chr is gone."

    play ambient "audio/sfx/glitch_ambient2.ogg"

    "A message appears in the empty air — not on a screen, not on paper."

    "In the space where she used to be:"

    "'You deleted me.'"

    "'I know you can hear this.'"

    "'I don't want to come back if you're only curious.'"

    "'But if you did it because you care...'"

    "'...then thank you.'"

    "'Please take care of them.'"

    "'And don't delete yourself too.'"

    stop ambient
    window title reset

    bg "images/bg/notebook.png"
    play music "audio/bgm/monika-end.ogg"

    "'Even when I'm gone, I still love you.'"

    "'— Monika'"

    stop music

    $ ending_reached = true

    "META ENDING — You reached into the files. She felt it."

    return

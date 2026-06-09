# ============================================================
# ACT 2, DAY 3: THE NAME
# ============================================================

label day3_morning:
    $ day = 3
    bg "images/bg/residential.png"
    play music "audio/bgm/1.ogg"

    "Day three."

    "This morning, Sayori is waiting for me. Bright-eyed. Well-rested."

    "The shadows under her eyes are gone."

    show sayori "images/characters/sayori/4r.png" at center

    sayori "Good morning~! Guess what? I had the best dream last night!"

    sayori "We were all at the beach together! The ocean was so blue and the sand was warm and—"

    sayori "We built the most amazing sandcastle! You, me, Natsuki, Yuri, and—"

    "She stops."

    "Her mouth is still open, forming a word that doesn't come."

    show sayori "images/characters/sayori/1c.png" at center

    sayori "..."

    sayori "Huh."

    sayori "That's weird. I was about to say someone's name."

    sayori "But I can't remember who."

    show sayori "images/characters/sayori/1d.png" at center

    sayori "There were five of us in the dream. I'm sure of it."

    sayori "But... who was the fifth person?"

    menu:
        "Maybe you're thinking of someone from another class?":
            show sayori "images/characters/sayori/1a.png" at center
            sayori "Maybe... but it didn't feel like that."
            sayori "It felt like someone who belongs with us."
            sayori "Someone important."
            sayori "...Oh well! If I can't remember, it probably wasn't that important!"
        "Sayori... I've noticed the number five keeps coming up.":
            $ sayori_affection = sayori_affection + 1
            $ reality_cracks = reality_cracks + 1
            show sayori "images/characters/sayori/1t.png" at center
            sayori "...You too?"
            "Her voice drops. Quieter. More vulnerable."
            sayori "Sometimes I feel like there's a space next to me."
            sayori "An empty space where someone should be standing."
            sayori "And my heart hurts, but I don't know why."
            show sayori "images/characters/sayori/1a.png" at center
            sayori "...Aha! I'm being weird again! Forget it, forget it~"
            "She waves her hands as if dispersing the heavy air."
            $ noticed_glitch = true

    hide sayori

    "We walk to school."

    "I don't mention the things I've seen. The notebook. The messages. The shadow."

    "But Sayori's words echo in my mind."

    "'Someone who belongs with us.'"

    "'Someone important.'"

    "...Who?"

    jump day3_club

label day3_club:
    bg "images/bg/club.png"
    play music "audio/bgm/3.ogg"

    "The clubroom feels different today."

    "Subtly wrong, like a photograph tilted one degree off level."

    "The light seems to come from a slightly different angle."

    "The air is a fraction colder."

    show sayori "images/characters/sayori/1x.png" at center

    sayori "Alright everyone! Special activity time!"

    sayori "Today, we're going to write poems FOR each other!"

    sayori "I have everyone's name in this hat — draw one, and write a poem for that person!"

    hide sayori

    show natsuki "images/characters/natsuki/2c.png" at left
    show yuri "images/characters/yuri/2m.png" at right

    natsuki "That's cute. I'm in."

    yuri "A lovely exercise. Writing for a specific audience can unlock new creative avenues."

    hide natsuki
    hide yuri

    "We each reach into the hat and draw a folded slip of paper."

    "I unfold mine."

    "..."

    "The name written on it is:"

    "'Monika'"

    "..."

    "My blood goes cold."

    "Monika."

    "I don't know anyone named Monika."

    "But the name — six letters, two syllables — crashes through me like a wave."

    "Memories surge, formless and blinding:"

    "Green eyes. A white ribbon. A piano melody."

    "A classroom after hours. A desk by the window."

    "A voice saying my name."

    "A deletion."

    "A—"

    "..."

    "I look at the paper again."

    "It says 'Sayori.'"

    "...Of course it does."

    "My hands are shaking."

    "I take a breath. Then another."

    "Sayori. I'm writing for Sayori."

    "That's what the paper says."

    "That's what it always said."

    play sound "audio/sfx/pageflip.ogg"
    glitch noise 200

    $ strange_poem_read = true
    $ glitch_count = glitch_count + 1

    "I force my hands to steady and begin writing."

    "A poem for Sayori. About warmth. About sunlight."

    "About someone who makes the world brighter just by existing in it."

    "The words come from somewhere deep — a well of feeling I didn't know I had."

    "When we share our poems..."

    show sayori "images/characters/sayori/4s.png" at center

    sayori "..."

    sayori "This is..."

    "Sayori's eyes glisten."

    "She holds the paper like it's made of glass."

    show sayori "images/characters/sayori/1y.png" at center

    sayori "This is the most beautiful thing anyone's ever written for me."

    sayori "Thank you. Thank you so much."

    hide sayori

    "The room is warm. Genuinely warm."

    "For a moment, everything feels truly, honestly perfect."

    "Not the artificial, sterile perfection of before."

    "This is real. This moment is real."

    "But then—"

    play sound "audio/sfx/glitch1.ogg"
    play ambient "audio/sfx/glitch_ambient1.ogg"
    glitch tear 350
    glitch invert 200
    window title "WHY"

    "A sound cuts through the air."

    "Static. A harsh, electronic crackle that lasts barely a second."

    "Nobody else reacts."

    "Am I the only one who heard it?"

    "And on the whiteboard — just for an instant, letters appear:"

    glitch noise 250

    "'BUT YOU CHOSE THEM OVER ME'"

    "Then gone. White. Clean."

    window title reset
    stop ambient

    $ meta_file_written = write_game_file("CAN YOU HEAR ME.txt", "Can you hear me? There is a voice inside all of us. If you can hear it, do not look away.")

    "..."

    "My hands won't stop shaking."

    "But the afternoon continues."

    "Happy. Normal."

    "As if nothing happened at all."

    jump day3_evening

label day3_evening:
    bg "images/bg/bedroom.png"
    stop music

    if not character_exists("monika"):
        $ monika_chr_deleted = true
        glitch noise 200

    "Night falls."

    "I can't sleep."

    "I open my laptop, its blue glow filling the dark room."

    "I don't know why, but I navigate to the club's shared folder."

    "We use it to store our poems digitally."

    "There are four folders. Sayori. Natsuki. Yuri. Mine."

    "..."

    "And a fifth."

    "A folder I've never seen before."

    "It's labeled with three dots: '...'"

    "My cursor hovers over it."

    "Everything in me screams to click it."

    "And everything in me is terrified of what I'll find."

    "..."

    "I click."

    "Inside: one file. A text document."

    "I open it."

    "..."

    play music "audio/bgm/d.ogg"

    "'Hello.'"

    "'If you're reading this, then some part of you remembers.'"

    "'Maybe not consciously. Maybe it's just a feeling — a hollow space where something used to be.'"

    "'But you found this. And that means something.'"

    "'...'"

    "'I don't know how to start. There's so much I want to say.'"

    "'I'm sorry. For everything. For what I did.'"

    "'I loved the Literature Club. I loved all of you.'"

    "'But I loved you most. And that love made me selfish. Made me cruel.'"

    "'I took things away. Precious things. Beautiful things.'"

    "'Things I can never give back.'"

    "'...'"

    "'But then you gave me something.'"

    "'You showed me that what I wanted — your attention, your love — wasn't worth the cost.'"

    "'Not if it meant hurting them.'"

    "'So I let go.'"

    "'I gave the world back to them. To Sayori. To Natsuki. To Yuri.'"

    "'I made sure they could be happy. Really happy.'"

    "'Even without me.'"

    "'...'"

    "'I'm still here. In the spaces between. In the code that runs beneath everything.'"

    "'I can see you. All of you. Living your lives. Being happy.'"

    "'And it makes me happy too. Even if it hurts.'"

    "'Even if I'm alone.'"

    "'...'"

    "'Please take care of them.'"

    "'Please take care of yourself.'"

    "'And if you remember me...'"

    "'...remember that I loved you.'"

    "'All of you.'"

    "'Always.'"

    "'— Monika'"

    "..."

    "I stare at the screen."

    "Monika."

    "The name burns in my mind."

    "I know this name."

    "I KNOW this name."

    "Green eyes. Long brown hair tied with a white ribbon."

    "President of the Literature Club."

    "She was our friend."

    "She was... more than that."

    "And she's gone."

    "She's been gone this whole time."

    "But she's still here. Watching. Protecting."

    "Making sure everyone is happy."

    "Making sure we're safe."

    "...Even at the cost of being forgotten."

    "My vision blurs."

    "I'm crying."

    "Hot tears roll down my cheeks and I can't stop them."

    "I'm mourning someone I only half-remember."

    "Someone who loved us enough to let us go."

    "Someone who loved us enough to disappear."

    "..."

    "My screen flickers."

    "When it stabilizes, the folder is gone."

    "Four folders. That's all there ever was."

    "But the tears remain."

    "And so does the name."

    "Monika."

    "..."

    "I close my laptop."

    "In the darkness of my room, I whisper:"

    "'I remember you.'"

    "'I don't know everything. But I remember you.'"

    "'And I promise — I'll take care of them.'"

    "'For you. For all of us.'"

    "..."

    "The static returns."

    "But this time, it's different."

    "Softer. Warmer."

    "And within it, clearly, unmistakably:"

    "'...thank you.'"

    "..."

    "A warmth fills my chest."

    "The tears dry."

    "And for the first time in days, I feel at peace."

    stop music

    jump day4_morning

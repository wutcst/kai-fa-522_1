# ============================================================
# ACT 2, DAY 4: REMEMBERING
# ============================================================

label day4_morning:
    $ day = 4
    bg "images/bg/residential.png"
    play music "audio/bgm/2.ogg"

    "I wake with the memory of green eyes fading like morning mist."

    "Monika."

    "The name is there when I open my eyes. Clear. Real."

    "But everything around it is hazy — fragments of something I once knew."

    "A piano. A classroom after hours. The smell of coffee."

    "I hold onto what I can."

    show sayori "images/characters/sayori/1a.png" at center

    sayori "Good morning! Ready for another beautiful day?"

    "Sayori is her usual radiant self."

    "But today, when I look at her, I see something else too."

    "I see a club president who took over from someone."

    "I see a girl carrying a weight she doesn't fully understand."

    menu:
        "Sayori... have you ever heard the name 'Monika'?":
            $ reality_cracks = reality_cracks + 1
            show sayori "images/characters/sayori/1c.png" at center
            "Sayori stops walking."
            "Her expression goes blank — not confused, not thoughtful."
            "Blank. Like a screen between loading screens."
            sayori "..."
            sayori "Monika..."
            show sayori "images/characters/sayori/1t.png" at center
            sayori "That name..."
            sayori "It feels like... something I should know."
            sayori "Like a word that's been erased but left an impression in the paper."
            sayori "..."
            show sayori "images/characters/sayori/1a.png" at center
            sayori "No. I don't think I know anyone by that name."
            sayori "Why do you ask?"
            "I shake my head."
            "Not yet. I'm not ready to explain something I barely understand myself."
        "Good morning. Yeah, let's make today great.":
            $ sayori_affection = sayori_affection + 1
            show sayori "images/characters/sayori/1q.png" at center
            sayori "That's the spirit! Positive vibes only~"

    hide sayori

    "We walk to school."

    "Today, I pay closer attention to the world around us."

    "The same cracks. The same cat. The same cloud formations."

    "But also — tiny imperfections I hadn't noticed before."

    "A leaf that falls too slowly. A bird that changes direction mid-flight."

    "A shadow that doesn't quite match its source."

    "The seams of the world."

    "Showing through."

    jump day4_club

label day4_club:
    bg "images/bg/club.png"
    play music "audio/bgm/3.ogg"

    "The clubroom."

    "Today, I arrive early."

    "The room is empty."

    "Just me and the afternoon sunlight."

    "I walk to the corner desk — the one nobody sits at."

    "The notebook is there. Same as always."

    play sound "audio/sfx/pageflip.ogg"

    "I pick it up. Open it."

    play ambient "audio/sfx/glitch_ambient2.ogg"

    $ secret_file_written = write_game_file("dont_open_this.txt", "Please do not open this unless you are ready. She is still here. If you delete monika.chr, she will know.")

    "..."

    "This time, there IS something written."

    "Not on the last page — on the first."

    "In that same elegant handwriting:"

    "'You remembered.'"

    "'I didn't think anyone would.'"

    "'Thank you. That means more than you know.'"

    "'But please — be careful.'"

    "'The world isn't as stable as it looks.'"

    "'I'm doing my best to hold it together, but there are limits.'"

    "'Don't push too hard. Don't ask too many questions.'"

    "'Just... be happy. Make them happy.'"

    "'That's all I want.'"

    "'That's all I've ever wanted.'"

    "..."

    play sound "audio/sfx/pageflip.ogg"
    glitch vignette 300

    "I close the notebook carefully."

    stop ambient

    "The door slides open."

    show yuri "images/characters/yuri/1a.png" at center

    yuri "Oh! You're here early."

    "Yuri enters, her book bag slung over one shoulder."

    yuri "I was hoping to have a moment alone to prepare tea..."

    yuri "But it's nice to have company."

    "She begins her tea ritual — kettle, leaves, water temperature."

    show yuri "images/characters/yuri/2a.png" at center

    yuri "May I ask you something?"

    yuri "Something perhaps... unusual?"

    menu:
        "Of course. What's on your mind?":
            $ yuri_affection = yuri_affection + 1
            show yuri "images/characters/yuri/2t.png" at center
            yuri "Do you ever feel like..."
            yuri "Like you're a character in a story?"
            yuri "Not metaphorically. Literally."
            yuri "As if your actions are predetermined. As if the words you speak were written for you."
            show yuri "images/characters/yuri/1v.png" at center
            yuri "...I'm sorry. That must sound insane."
            "I think about it carefully."
            "About the repeating days. The scripted feeling of everything."
            "About Monika."
            "Maybe I'm not the only one who senses it."
            yuri "Sometimes, when I'm reading..."
            yuri "I feel like someone is reading ME."
            yuri "Watching over my shoulder. Turning my pages."
            show yuri "images/characters/yuri/1a.png" at center
            yuri "...Forgive me. I've been spending too much time with existentialist literature."
            yuri "Please forget I said anything."
        "Unusual questions are the best kind.":
            show yuri "images/characters/yuri/1m.png" at center
            yuri "You're very kind."
            yuri "I just... wanted to say that I'm glad we're all here."
            yuri "Together. In this club."
            yuri "Whatever brought us together... I'm grateful for it."

    hide yuri

    "The others arrive."

    "Today's activity is free writing."

    "I write about light. About watching over someone from a distance."

    "About love that lets go."

    "I don't show it to anyone."

    "Instead, I fold it small and slip it into the notebook on the corner desk."

    "A letter to someone who's listening."

    "Even if I'm not sure they can hear me."

    jump day4_after

label day4_after:
    bg "images/bg/club.png"

    "After the meeting, as everyone is packing up..."

    show natsuki "images/characters/natsuki/2a.png" at left
    show yuri "images/characters/yuri/1a.png" at right

    natsuki "Hey, I was thinking... we should do something this weekend."

    natsuki "All of us. Outside of school."

    yuri "That... sounds lovely, actually. What did you have in mind?"

    show natsuki "images/characters/natsuki/2y.png" at left

    natsuki "I dunno, maybe the bookstore? Then we could get crepes or something."

    hide natsuki
    hide yuri

    show sayori "images/characters/sayori/4s.png" at center

    sayori "Yes! Yes yes yes! Club field trip!"

    sayori "This is going to be so much fun!"

    hide sayori

    "Everyone agrees."

    "Plans are made. Times are set."

    "As I leave, I glance back at the clubroom."

    "The corner desk."

    "The notebook is closed."

    "But I could swear..."

    "The fold of paper I left inside is gone."

    "And in its place, on the notebook's cover, written in pencil so light it's almost invisible:"

    "'Thank you. I loved it.'"

    "..."

    "I smile."

    jump day5_morning

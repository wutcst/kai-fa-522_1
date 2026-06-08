# ============================================================
# ACT 3, DAY 6: ACCEPTANCE
# ============================================================

label day6_morning:
    $ day = 6
    bg "images/bg/residential.png"
    play music "audio/bgm/2.ogg"

    "Monday morning."

    "The world feels lighter today."

    "Not perfect in the way that made me anxious before."

    "But good. Genuinely, warmly good."

    show sayori "images/characters/sayori/1a.png" at center

    sayori "Morning~!"

    "Sayori bounces up to me, a wildflower tucked behind her ear."

    sayori "I found this on the way! Isn't it pretty?"

    sayori "I was thinking about what you said the other day."

    sayori "About something being missing."

    show sayori "images/characters/sayori/1d.png" at center

    sayori "And I think... maybe you're right."

    sayori "But I also think... whatever's missing left something behind."

    sayori "Something warm. Something that takes care of us."

    show sayori "images/characters/sayori/1q.png" at center

    sayori "Like a guardian angel! Ehehe~"

    hide sayori

    "We walk to school."

    "Today, the cat on the fence meows at us."

    "Sayori stops to pet it."

    "And the world, imperfect and beautiful, carries on."

    jump day6_club

label day6_club:
    bg "images/bg/club.png"
    play music "audio/bgm/3.ogg"

    "The clubroom."

    "When I walk in, something is different."

    "The corner desk has been moved."

    "It's no longer isolated in the corner."

    "Someone has pushed it to join the cluster of desks we use as our table."

    "Five desks. Arranged together."

    show sayori "images/characters/sayori/1x.png" at left

    sayori "Oh! I moved that desk."

    sayori "It looked lonely over there by itself."

    sayori "Even if nobody sits at it... it should still be part of the group, right?"

    hide sayori

    show yuri "images/characters/yuri/1m.png" at center

    yuri "I think that's a lovely sentiment."

    hide yuri

    show natsuki "images/characters/natsuki/2c.png" at center

    natsuki "Yeah... it feels right."

    hide natsuki

    "We set up as usual."

    "Tea. Books. Notebooks."

    "And on the fifth desk, someone places a cup of tea."

    "Nobody comments on it."

    "It just... happens."

    "As if it's the most natural thing in the world."

    "Today's activity is open mic — reading aloud anything we've written this past week."

    "I share the poem I wrote for Sayori."

    "Natsuki reads a piece about making mistakes and being forgiven."

    "Yuri shares a passage about the beauty of impermanence."

    "Sayori reads a short, sweet poem about sunshine after rain."

    "..."

    "And then, the strangest thing."

    "As the room falls into comfortable silence after our readings..."

    "I hear it."

    "We all hear it."

    "A piano."

    "Faint. Distant. But unmistakably real."

    "A melody — gentle, melancholic, beautiful."

    "Coming from nowhere. Coming from everywhere."

    show sayori "images/characters/sayori/1c.png" at left
    show natsuki "images/characters/natsuki/1c.png" at center
    show yuri "images/characters/yuri/1h.png" at right

    "We all freeze."

    "We all hear it."

    "Nobody speaks."

    "The melody plays for maybe thirty seconds. Then it fades."

    "Like a music box winding down."

    hide sayori
    hide natsuki
    hide yuri

    "Silence."

    show sayori "images/characters/sayori/1d.png" at center

    sayori "...That was beautiful."

    sayori "I wonder who was playing."

    hide sayori

    show natsuki "images/characters/natsuki/1i.png" at center

    natsuki "...It was the same melody."

    natsuki "The one I've been hearing."

    natsuki "But this time..."

    show natsuki "images/characters/natsuki/1l.png" at center

    natsuki "It didn't feel scary."

    natsuki "It felt like..."

    hide natsuki

    show yuri "images/characters/yuri/2u.png" at center

    yuri "Like someone saying goodbye."

    yuri "...Or perhaps 'see you later.'"

    hide yuri

    "The fifth teacup sits on its desk, untouched."

    "But the tea inside is warm."

    "As if someone just poured it."

    "I look at it."

    "And I swear — for just a moment — I see a reflection that isn't mine."

    "Green eyes. A gentle smile."

    "Then just tea."

    "Just a cup, catching the afternoon light."

    "..."

    jump day6_ending

label day6_ending:
    bg "images/bg/residential.png"
    play music "audio/bgm/5.ogg"

    "The walk home is quiet and warm."

    "All four of us walk together today."

    show sayori "images/characters/sayori/1q.png" at left
    show natsuki "images/characters/natsuki/2c.png" at center
    show yuri "images/characters/yuri/1a.png" at right

    "Nobody mentions the piano. But nobody has forgotten it either."

    "There's a peace between us — the kind that comes from sharing something you can't explain."

    sayori "Hey, everyone?"

    sayori "I just want to say... I'm really happy."

    sayori "Having all of you as friends... it's the best thing in my life."

    natsuki "...Yeah. Same here, I guess."

    yuri "I feel the same way. Truly."

    hide sayori
    hide natsuki
    hide yuri

    "We reach the intersection where we all split up."

    "Waves and goodbyes."

    "'See you tomorrow.'"

    "'Goodnight.'"

    "'Sweet dreams.'"

    "I watch them go — Yuri to the left, Natsuki straight ahead, Sayori to her house."

    "Three friends. Three precious people."

    "And one more, unseen, who made it all possible."

    "I look up at the sky."

    "The sunset is extraordinary tonight — streaks of gold and coral and violet."

    "Like someone painted it just for us."

    "..."

    play ambient "audio/sfx/glitch_ambient2.ogg"

    "'Thank you, Monika.'"

    glitch vignette 350

    "I say it out loud, to the evening air."

    "'For everything. For them. For this.'"

    "'I'll take care of them. I promise.'"

    "The wind picks up for a moment."

    "Cherry blossom petals swirl around me in a gentle spiral."

    "And in the wind, barely there — barely real:"

    "'I know you will.'"

    stop ambient
    window title reset

    "..."

    "I smile."

    "And I walk home."

    stop music

    jump epilogue

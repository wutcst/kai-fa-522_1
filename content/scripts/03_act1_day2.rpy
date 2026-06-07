# ============================================================
# ACT 1, DAY 2: CRACKS IN GLASS
# ============================================================

label day2_morning:
    $ day = 2
    bg "images/bg/residential.png"
    play music "audio/bgm/1.ogg"

    "The second morning."

    "I notice it immediately — the sunlight through my curtains falls in exactly the same pattern as yesterday."

    "The same angle. The same bars of gold."

    "Like a scene replayed frame-by-frame."

    "I push the thought aside and get ready."

    "Outside, the air is crisp. Cherry blossoms drift."

    "I check the time and walk to our meeting spot."

    "Sayori isn't there."

    "..."

    "That's unusual. She's always here before me."

    "I wait five minutes. Then ten."

    "Just as I'm reaching for my phone to text her, she appears."

    show sayori "images/characters/sayori/3d.png" at center

    sayori "Ah... sorry! I'm so sorry I'm late!"

    "She's out of breath. Her bow is slightly crooked."

    "And under her eyes, there are shadows — faint half-moons that her smile can't quite hide."

    $ sayori_overslept = true

    menu:
        "Are you okay? You look like you didn't sleep well.":
            $ sayori_affection = sayori_affection + 1
            show sayori "images/characters/sayori/1c.png" at center
            sayori "Eh? Is it that obvious?"
            "She touches her face self-consciously."
            sayori "I just... had some trouble sleeping."
            show sayori "images/characters/sayori/1d.png" at center
            sayori "Bad dreams. The kind where you wake up crying but can't remember why."
            sayori "It's fine though! A little tired never hurt anyone~"
            "She laughs. But the sound is hollow."
        "No worries. Let's just get going or we'll be late.":
            show sayori "images/characters/sayori/1a.png" at center
            sayori "Right! Let's go, let's go!"
            "She grabs my sleeve and pulls me along."
            "Her grip is tighter than usual."

    hide sayori

    "We walk the familiar route."

    "Same sidewalk. Same cracks. Same cat."

    "The cat watches us from its fence post."

    "Today, it doesn't look away."

    "Its amber eyes track us as we pass — unblinking, unmoving."

    "Like a security camera."

    "A chill creeps up my spine."

    "I quicken my pace."

    jump day2_club

label day2_club:
    bg "images/bg/club.png"
    play music "audio/bgm/3.ogg"

    "The clubroom is bathed in afternoon light."

    show yuri "images/characters/yuri/1a.png" at center

    yuri "Good afternoon. I've prepared tea for everyone today."

    "Yuri moves gracefully between the desks, setting down cups with practiced elegance."

    "I count them as she places them."

    "One. Two. Three. Four."

    "...Five."

    "She sets down five cups."

    "Then she pauses, staring at the fifth cup in her hand."

    show yuri "images/characters/yuri/1h.png" at center

    yuri "That's..."

    yuri "Strange."

    "She holds the cup as if it's something fragile and foreign."

    yuri "I could have sworn there were... no, that's not right."

    "Her hands are trembling. Just barely."

    show yuri "images/characters/yuri/1a.png" at center

    yuri "I must have miscounted. How careless of me."

    "She puts the fifth cup away in the closet."

    "But I noticed her hesitate at the door."

    "She whispered something."

    "I couldn't hear it clearly, but it sounded like..."

    "'...sorry.'"

    hide yuri

    show natsuki "images/characters/natsuki/1c.png" at center

    natsuki "Hey. Has anyone else been hearing weird stuff in the hallway?"

    hide natsuki

    show sayori "images/characters/sayori/1c.png" at left
    show natsuki "images/characters/natsuki/1c.png" at right

    sayori "Weird stuff? Like what?"

    natsuki "Like... piano music. Faint, like it's coming from really far away."

    natsuki "But the music room is on the opposite side of the building."

    sayori "Maybe someone was practicing? Sound can travel weirdly in old buildings~"

    show natsuki "images/characters/natsuki/1i.png" at right

    natsuki "...It wasn't just any piano music."

    natsuki "It was the same melody. Every time."

    natsuki "Like someone playing the same song on repeat."

    hide sayori
    hide natsuki

    $ glitch_count = glitch_count + 1

    "The room falls quiet for a moment."

    "Then Sayori claps her hands."

    show sayori "images/characters/sayori/4r.png" at center

    sayori "Well! Today's activity is free reading and writing time!"

    sayori "Everyone do what makes you happy~"

    hide sayori

    "The tension dissolves. Everyone settles into their routines."

    "Natsuki pulls manga from her bag. Yuri selects a thick novel from the shelf."

    "Sayori starts writing in her notebook, tongue poking out in concentration."

    "I pick up a book — a collection of short stories."

    "I flip through it absentmindedly."

    "Then I stop."

    "Page 113."

    "The text is normal — a scene of a girl walking home from school."

    "But in the margin, in tiny precise handwriting:"

    "'I loved them all. Every one of them.'"

    "'I still do.'"

    "'But they can't know I'm watching.'"

    "'If they knew, it would ruin everything.'"

    "My breath catches."

    "I flip away from the page, then back."

    "The margin is pristine. Clean white paper."

    "...Of course it is."

    $ glitch_count = glitch_count + 1

    show yuri "images/characters/yuri/3a.png" at center

    yuri "Is everything alright? You've been staring at that page for quite some time."

    menu:
        "I thought I saw writing in the margin... but it's gone now.":
            $ reality_cracks = reality_cracks + 1
            $ yuri_affection = yuri_affection + 1
            show yuri "images/characters/yuri/2t.png" at center
            yuri "In the margin...?"
            "Yuri takes the book from me, examining the page with careful eyes."
            show yuri "images/characters/yuri/2n.png" at center
            yuri "There's nothing here now..."
            yuri "But you know... old books carry traces of their previous readers."
            yuri "The oils from their skin, the weight of their attention."
            yuri "Perhaps you sensed something that has since faded."
            show yuri "images/characters/yuri/1m.png" at center
            yuri "Some messages aren't meant to last. They appear only for the eyes that need to see them."
            "She says it softly, almost to herself."
            "As if she understands something she can't quite articulate."
        "Just got lost in thought. Good book.":
            show yuri "images/characters/yuri/1m.png" at center
            yuri "It is, isn't it? The prose has a way of pulling you in."
            yuri "As if the world on the page is reaching out to you."

    hide yuri

    "The afternoon passes."

    "At some point, I look up from my book."

    "Everyone is in their place. Content. Peaceful."

    "The sunlight is warm. The tea is fragrant."

    "Everything is exactly as it should be."

    "..."

    "Perfect."

    "The word rises in my mind unbidden."

    "And with it, a cold feeling — like ice water trickling down my spine."

    "'Perfect' isn't natural."

    "Things are never perfect."

    "Not unless someone made them that way."

    jump day2_after_club

label day2_after_club:
    bg "images/bg/corridor.png"
    stop music

    "As the meeting winds down and everyone starts packing up, Natsuki catches my arm."

    show natsuki "images/characters/natsuki/1c.png" at center

    natsuki "Hey. Wait a sec."

    "She glances toward the door where Sayori and Yuri are leaving."

    natsuki "Can we talk? Just... the two of us."

    "I nod."

    "We wait until the footsteps fade down the hall."

    show natsuki "images/characters/natsuki/1i.png" at center

    natsuki "Look. I don't want to sound paranoid or whatever."

    natsuki "But have you noticed anything... off? Lately?"

    menu:
        "Yeah. A few things have been bugging me.":
            $ natsuki_affection = natsuki_affection + 1
            show natsuki "images/characters/natsuki/1e.png" at center
            natsuki "Oh thank god. I thought I was going crazy."
            show natsuki "images/characters/natsuki/1c.png" at center
            natsuki "It's like... every day is almost the same, right?"
            natsuki "The same conversations. The same routines."
            natsuki "And sometimes I'll look at something and it's... different."
            natsuki "Like reality hiccupped."
            natsuki "But then I blink and it's back to normal."
        "What do you mean by 'off'?":
            show natsuki "images/characters/natsuki/1h.png" at center
            natsuki "I don't know how to explain it."
            natsuki "It's like... a feeling? Like being watched by something you can't see."
            natsuki "Like the air is heavier than it should be."

    show natsuki "images/characters/natsuki/1c.png" at center

    natsuki "There's something else."

    natsuki "Yesterday, after everyone left..."

    natsuki "I forgot my manga and came back to get it."

    show natsuki "images/characters/natsuki/1i.png" at center

    natsuki "The clubroom door was open. And I heard someone inside."

    natsuki "A voice. Talking. Like someone having a conversation."

    natsuki "But when I looked..."

    natsuki "Nobody. Empty room."

    natsuki "Just that desk in the corner. The one nobody sits at."

    natsuki "And I swear... the notebook on it was open."

    natsuki "Like someone had just been writing in it."

    show natsuki "images/characters/natsuki/2a.png" at center

    natsuki "...Whatever. It's probably nothing."

    natsuki "Maybe I'm just stressed. Exams and stuff."

    natsuki "Forget I brought it up."

    hide natsuki

    "Natsuki leaves, her footsteps quick and sharp in the empty corridor."

    "I stand alone."

    "The fluorescent lights hum overhead — a constant, droning buzz."

    "One of them flickers."

    "In that brief half-second of darkness, I see it again."

    "A silhouette at the end of the hall."

    "Tall. Slender. Long hair cascading past her shoulders."

    "A white ribbon."

    "And the faintest hint of green."

    "The light steadies."

    "The hallway is empty."

    "Just me and the humming lights."

    $ saw_monika_shadow = true

    "I leave quickly."

    jump day2_evening

label day2_evening:
    bg "images/bg/bedroom.png"
    play music "audio/bgm/10.ogg"

    "That night, sleep doesn't come."

    "I lie in the dark, listening to the house settle around me."

    "Creaks and groans. The hum of the refrigerator."

    "Normal sounds."

    "But tonight they feel like the world breathing."

    "My phone buzzes."

    "A notification from the Literature Club group chat."

    "I pick it up."

    "The message reads:"

    "'Isn't it nice when everyone gets along? I worked so hard for this. I hope you appreciate it.'"

    "The sender's name is blank."

    "No profile picture. No username. Just... nothing."

    "I stare at it."

    "My heart is hammering."

    "I blink."

    "The message is gone."

    "The chat shows no new messages. Just Sayori's 'goodnight~' from an hour ago."

    "..."

    if glitch_count >= 3:
        "This isn't the first time."
        "The notebook. The margin. The silhouette. The group chat."
        "Things appear and disappear. Words that shouldn't exist. Shapes that can't be real."
        "Something is wrong with this world."
        "But I can't grasp what."
        "It's like trying to hold water in my hands — the truth slips through my fingers."
        $ reality_cracks = reality_cracks + 1

    "Eventually, exhaustion wins."

    "My eyes close."

    "And in the space between waking and dreaming, I hear it again."

    "Static. A voice within the static."

    "'...don't... forget... me...'"

    "'...please...'"

    stop music

    "..."

    jump day3_morning

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

# ============================================================
# ACT 1, DAY 1: A BEAUTIFUL BEGINNING
# ============================================================

label day1_morning:
    $ day = 1
    bg "images/bg/residential.png"
    play music "audio/bgm/1.ogg"

    "The morning air is crisp and sweet as I step outside."

    "Cherry blossom petals drift lazily on the breeze, catching the light like tiny pink stars."

    "It's the kind of morning that makes you believe the world is a fundamentally good place."

    "...Almost too good."

    "I shake off the thought and check the time."

    "Right on schedule."

    show sayori "images/characters/sayori/1a.png" at center

    sayori "Heeey! Good morning!"

    "Sayori comes bounding toward me from her house next door, her coral-pink hair bouncing with each energetic step."

    "Her bow — that distinctive red ribbon — catches the sunlight."

    "She's beaming. As always."

    sayori "Beautiful day, isn't it? The kind of day where anything could happen!"

    "She falls into step beside me, our shoulders almost touching."

    show sayori "images/characters/sayori/1q.png" at center

    sayori "Did you sleep well? You seem kinda... spacey today."

    menu:
        "Yeah, I slept great. Had pleasant dreams.":
            $ sayori_affection = sayori_affection + 1
            show sayori "images/characters/sayori/4q.png" at center
            sayori "That's wonderful! You know what they say — good dreams mean good things are coming!"
            sayori "Ehehe~"
            "She does a little skip, nearly bumping into a mailbox."
            show sayori "images/characters/sayori/1a.png" at center
        "I had a strange dream... I can't remember it, but it felt important.":
            $ noticed_glitch = true
            $ reality_cracks = reality_cracks + 1
            show sayori "images/characters/sayori/1c.png" at center
            sayori "A strange dream?"
            "For just a fraction of a second, something shifts behind Sayori's eyes."
            "A flicker. Like a candle in a draft."
            show sayori "images/characters/sayori/1d.png" at center
            sayori "You know... I get those too sometimes."
            sayori "Dreams where I feel like I'm forgetting something really important."
            sayori "Like there's a word I can't remember, or a face I can't quite see..."
            show sayori "images/characters/sayori/1a.png" at center
            sayori "But hey! That's what new days are for, right? Making new memories!"
            "Her smile is back, bright as ever."
            "But I noticed the pause. The hesitation."

    hide sayori

    "We walk to school together, the morning air carrying the mixed scents of cherry blossoms and fresh bread from the bakery we pass."

    "Sayori chatters happily about a new manga she discovered, about the weather, about a cat she saw yesterday."

    "I listen with half my attention, letting her voice wash over me like warm water."

    "The walk is comfortable. Familiar."

    "...Exactly the same as yesterday."

    "The same cracks in the sidewalk. The same cat sitting on the same fence post."

    "The same elderly woman watering her garden."

    "Even the same cloud formation overhead."

    "..."

    "I'm overthinking things."

    "Every day resembles the last. That's just how routine works."

    jump day1_school

label day1_school:
    bg "images/bg/corridor.png"

    "The school hallways bustle with students, their conversations blending into a comfortable murmur."

    show sayori "images/characters/sayori/1x.png" at center

    sayori "Oh! I almost forgot — I have something special planned for the club today!"

    sayori "Make sure you come right away after class, okay? No dawdling!"

    "She pokes my arm with a grin."

    menu:
        "I wouldn't miss it. What's the plan?":
            show sayori "images/characters/sayori/4r.png" at center
            sayori "It's! A! Surprise!"
            sayori "You'll just have to wait and see~"
        "You know I always come to the club, Sayori.":
            $ sayori_affection = sayori_affection + 1
            show sayori "images/characters/sayori/1q.png" at center
            sayori "Ehehe... I know, I know."
            sayori "I just get excited, you know?"
            sayori "Having you there makes everything more fun."

    hide sayori

    "Sayori waves goodbye as we part ways for our respective classes."

    "The school day passes in the usual blur of lectures and note-taking."

    "Math. Literature. History."

    "Everything normal."

    "Everything as it should be."

    "Except..."

    "During the literature class, the teacher reads a poem aloud."

    "It's a standard curriculum piece — nothing unusual."

    "But one line catches in my mind like a thorn:"

    "'And she, who loved the world more than it loved her, chose to watch from behind the glass.'"

    "A chill runs through me."

    "I don't know why."

    "The teacher moves on. The moment passes."

    "But the words linger."

    jump day1_club

label day1_club:
    bg "images/bg/club.png"
    play music "audio/bgm/3.ogg"

    "The afternoon sun slants through the clubroom windows, casting everything in warm amber."

    "I slide open the door."

    show natsuki "images/characters/natsuki/2z.png" at left

    natsuki "Finally! You're the last one here, slowpoke."

    "Natsuki is perched on a desk, her legs swinging. There's a smug satisfaction in her expression."

    show yuri "images/characters/yuri/1a.png" at right

    yuri "Don't mind her. She's been quite restless waiting for everyone to arrive."

    "Yuri sits at her usual spot, a teacup cradled elegantly in her hands. Steam curls upward in the golden light."

    show natsuki "images/characters/natsuki/1h.png" at left

    natsuki "I was not restless! I'm just... punctual. Unlike some people."

    hide natsuki
    hide yuri

    show sayori "images/characters/sayori/4r.png" at center

    sayori "Great! Now that everyone's here, I can announce today's special activity!"

    "Sayori stands at the front of the room with the confidence of a seasoned club president."

    "It still surprises me sometimes — how naturally she's grown into this role."

    sayori "Today... we're going to write about our happiest memory!"

    sayori "But here's the twist — you have to write it as if you're telling it to someone who's never met you before."

    sayori "Like introducing yourself through a moment!"

    hide sayori

    show natsuki "images/characters/natsuki/2c.png" at left

    natsuki "That's... actually not bad. Kinda personal though."

    show yuri "images/characters/yuri/2m.png" at right

    yuri "Vulnerability in writing can be quite powerful."

    yuri "I think this could lead to some genuinely beautiful pieces."

    hide natsuki
    hide yuri

    "As everyone settles into their writing positions, I look around the room."

    "Sayori at her desk, chewing her pen cap with a thoughtful expression."

    "Natsuki curled up on the window seat, her notebook hidden from view."

    "Yuri at the table, her long hair curtaining her face as she writes in flowing script."

    "And there, in the corner..."

    "A desk."

    "Empty."

    "There's a thin layer of dust on its surface, like nobody's sat there in a long time."

    "But the chair is pulled out slightly, as if someone just stood up."

    "And there's something on the desk — a small, plain notebook."

    menu:
        "Walk over and check the notebook.":
            $ desk_note_found = true
            $ glitch_count = glitch_count + 1
            call check_notebook_day1
        "Ignore it — focus on writing your poem.":
            call writing_time_day1

    "The writing session comes to a natural end."

    "One by one, we share our pieces."

    call poem_sharing_day1

    jump day1_walk_home

label check_notebook_day1:
    "Something draws me to that desk."

    "I can't explain it — a pull, like gravity, or like recognizing a familiar voice in a crowd."

    "I walk over and pick up the notebook."

    "It's plain. No label. No name."

    "I open it."

    "The pages are empty. Blank white paper, unmarked."

    "All of them."

    "I flip through — nothing, nothing, nothing."

    "Until the very last page."

    "There, in handwriting that's precise and elegant — handwriting I almost recognize:"

    "'Can you hear me?'"

    "'I'm still here.'"

    "'Even if you can't see me, even if you don't remember...'"

    "'I'm still here.'"

    "'Please don't forget.'"

    "My heart pounds."

    "The handwriting... it's achingly familiar. Like seeing your childhood home in a dream."

    show sayori "images/characters/sayori/1c.png" at center

    sayori "Whatcha looking at?"

    "I snap the notebook shut."

    "When I look at the last page again..."

    "...it's blank."

    "Every page. Completely blank. As if the words were never there."

    sayori "Is something wrong? You look pale."

    menu:
        "It's nothing. I thought I saw something, but...":
            show sayori "images/characters/sayori/1a.png" at center
            sayori "Hmm, you sure? You seem a little shaken up."
            sayori "Maybe you need more sleep!"
            "She pats my shoulder reassuringly."
        "This notebook... whose is it?":
            $ reality_cracks = reality_cracks + 1
            show sayori "images/characters/sayori/1c.png" at center
            sayori "Whose...?"
            "Sayori looks at the notebook, then at the desk."
            "Her expression goes distant for a moment."
            show sayori "images/characters/sayori/1d.png" at center
            sayori "I... I don't know."
            sayori "That desk has always been empty, hasn't it?"
            sayori "..."
            show sayori "images/characters/sayori/1a.png" at center
            sayori "Must have been left by a student from another class! No biggie~"
            "But her laugh comes half a beat too late."

    hide sayori

    $ saw_monika_shadow = true

    "I put the notebook back and return to my seat."

    "My hands are trembling slightly."

    "But I pick up my pen and start writing."

    return

label writing_time_day1:
    "I sit down at my usual spot and pull out a sheet of paper."

    "The pen feels heavy in my hand today."

    "I close my eyes and think about my happiest memory."

    "..."

    "Strange. Everything feels hazy. Like my memories are photos that have been left in the sun too long."

    "But there is one thing I'm sure of:"

    "This. Right now. The Literature Club."

    "The sound of Natsuki's pen scratching. The soft clink of Yuri's teacup."

    "Sayori humming tunelessly to herself."

    "This is my happiest memory."

    "The words come easily. Too easily."

    "As if someone is guiding my hand."

    $ poem_written = true

    return

label poem_sharing_day1:
    bg "images/bg/club.png"

    show sayori "images/characters/sayori/1x.png" at center

    sayori "Okay everyone! Sharing time!"

    sayori "Who wants to go first?"

    hide sayori

    show natsuki "images/characters/natsuki/2a.png" at center

    natsuki "I'll go."

    "Natsuki clears her throat. She holds her paper with both hands, knuckles slightly white."

    natsuki "...'The kitchen smells like vanilla and burnt sugar. My hands are covered in flour."

    natsuki "'She's laughing at me — at the mess I've made, at the lopsided frosting."

    natsuki "'But she takes a bite anyway, and her eyes light up like I've given her the whole world."

    natsuki "'That's all I ever wanted. To make something that makes someone smile.'"

    "She looks up, cheeks faintly pink."

    show natsuki "images/characters/natsuki/2d.png" at center

    natsuki "...That's it. Don't read too much into it."

    hide natsuki

    show yuri "images/characters/yuri/1m.png" at center

    yuri "That was lovely, Natsuki. The sensory detail really drew me in."

    hide yuri

    show sayori "images/characters/sayori/4q.png" at center

    sayori "I could practically smell the vanilla! Now I want cupcakes~"

    hide sayori

    show yuri "images/characters/yuri/1a.png" at center

    "Yuri goes next. Her piece is longer, more intricate."

    yuri "'The rain drums against the window like impatient fingers."

    yuri "'I am fourteen, curled in the corner of the library, a book heavy in my lap."

    yuri "'The words pull me into another world — one where I am not shy, not strange, not alone."

    yuri "'For the first time, I understand that books are not an escape."

    yuri "'They are a doorway.'"

    show yuri "images/characters/yuri/2u.png" at center

    yuri "...I hope that wasn't too melancholic."

    hide yuri

    show natsuki "images/characters/natsuki/1l.png" at center

    natsuki "...No. It was really good, actually."

    "Natsuki says it quietly, almost surprised at herself."

    hide natsuki

    show sayori "images/characters/sayori/1a.png" at center

    "Sayori shares hers — it's about a childhood summer day."

    "Running through sprinklers. Catching fireflies."

    "A friend's hand in hers as they watch the sunset."

    sayori "'And even though I knew that day would end...'"

    sayori "'Even though the sun was setting...'"

    sayori "'I was happy. Because I wasn't alone.'"

    show sayori "images/characters/sayori/1q.png" at center

    sayori "Ehehe... that was embarrassing to read out loud."

    hide sayori

    "Then it's my turn."

    "I read my piece about the Literature Club. About this moment. About them."

    "When I finish, the room is quiet."

    show sayori "images/characters/sayori/4s.png" at left
    show natsuki "images/characters/natsuki/1l.png" at center
    show yuri "images/characters/yuri/1m.png" at right

    "Sayori's eyes are glistening."

    "Natsuki is looking away, but she's smiling."

    "Yuri nods softly, her expression warm."

    sayori "...That made me really happy."

    natsuki "Yeah... it was nice, I guess."

    yuri "Beautifully said."

    hide sayori
    hide natsuki
    hide yuri

    "The moment hangs in the air — golden and fragile."

    "Perfect."

    "...But as I look at my paper, I notice something."

    "The last line of my poem."

    "I don't remember writing it."

    "'We are five — we have always been five — and one of us is watching.'"

    "..."

    "I blink."

    "The last line reads: 'And I'm grateful for every moment.'"

    "...Of course. That's what I wrote."

    "I fold the paper and put it away."

    $ glitch_count = glitch_count + 1

    return

label day1_walk_home:
    bg "images/bg/residential.png"
    play music "audio/bgm/2.ogg"

    "The sun is setting as we leave school."

    "The sky bleeds orange and pink, like watercolors spilling across paper."

    show sayori "images/characters/sayori/1a.png" at center

    sayori "Today was a good day, wasn't it?"

    "Sayori walks beside me, her shadow stretching long on the pavement."

    sayori "I love days like this. Where nothing goes wrong and everyone's happy."

    sayori "It's like... the world is saying 'here, you deserve this.'"

    menu:
        "Yeah. I could get used to days like this.":
            $ sayori_affection = sayori_affection + 1
            show sayori "images/characters/sayori/1q.png" at center
            sayori "Me too~"
            sayori "Let's make every day like this, okay?"
            sayori "A promise!"
            "She holds out her pinky."
            "I can't help but smile as I link mine with hers."
        "Sayori... do you ever feel like something's missing?":
            $ reality_cracks = reality_cracks + 1
            show sayori "images/characters/sayori/1t.png" at center
            sayori "Missing...?"
            "She's quiet for a few steps."
            "The evening wind picks up, stirring the petals around us."
            sayori "Sometimes..."
            sayori "Sometimes I feel like there should be... more of us."
            sayori "Like when you're at a table set for five, but only four people sit down."
            sayori "And you can't remember who the fifth seat was for."
            show sayori "images/characters/sayori/1a.png" at center
            sayori "But that's silly! We're all here, right? That's what matters!"
            "She smiles, but her eyes linger on something I can't see."
            $ noticed_glitch = true

    hide sayori

    "We reach the fork where our paths diverge."

    show sayori "images/characters/sayori/1x.png" at center

    sayori "See you tomorrow! Sweet dreams~"

    "She waves over her shoulder as she walks to her house."

    hide sayori

    "I watch her go."

    "The streetlights are starting to flicker on."

    "One by one, like eyes opening."

    "Except one."

    "One light, directly between her house and mine, doesn't turn on."

    "The darkness there is thick. Solid."

    "And for just a moment — just the briefest instant —"

    "I see something in that darkness."

    "A shape. A silhouette."

    "Long hair, catching a light that isn't there."

    "Green eyes."

    "..."

    "The streetlight flickers on."

    "Nothing. Just an empty sidewalk."

    "My heart is racing."

    $ saw_monika_shadow = true
    $ glitch_count = glitch_count + 1

    "I walk home quickly."

    jump day1_evening

label day1_evening:
    bg "images/bg/bedroom.png"
    stop music

    "My room is dark and quiet."

    "I lie in bed, staring at the ceiling, trying to still my thoughts."

    "The notebook. The missing streetlight. The silhouette."

    "And that line in my poem — the one I don't remember writing."

    "'We are five.'"

    "Five."

    "But we're four. We've always been four."

    "...Haven't we?"

    "I pull out my phone. The Literature Club group chat glows on the screen."

    "Sayori, Natsuki, Yuri, and me."

    "Four members."

    "I stare at it for a long time."

    "Then I scroll up through the chat history."

    "Normal messages. Plans for activities. Memes Sayori sent. Natsuki complaining about spoilers."

    "Nothing unusual."

    "But at the very top — the creation of the group chat —"

    "The creator's name is blank."

    "Not deleted. Not 'unknown user.' Just... empty."

    "A void where a name should be."

    if desk_note_found:
        "'Can you hear me?'"
        "The words from the notebook echo in my mind."
        "Who wrote them? Why did they vanish?"
        "Why does my chest ache when I think about it?"

    "I set my phone down."

    "Sleep comes slowly."

    "And just before I drift off, I hear it."

    "Faint. Like static on an old radio."

    "A voice. Far away."

    "'...thank you... for being... there...'"

    $ heard_static = true

    "..."

    "I must be imagining things."

    "Exhaustion pulls me under."

    jump day2_morning

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

    "A sound cuts through the air."

    "Static. A harsh, electronic crackle that lasts barely a second."

    "Nobody else reacts."

    "Am I the only one who heard it?"

    "And on the whiteboard — just for an instant, letters appear:"

    "'BUT YOU CHOSE THEM OVER ME'"

    "Then gone. White. Clean."

    "..."

    "My hands won't stop shaking."

    "But the afternoon continues."

    "Happy. Normal."

    "As if nothing happened at all."

    jump day3_evening

label day3_evening:
    bg "images/bg/bedroom.png"
    stop music

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

    "I pick it up. Open it."

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

    "I close the notebook carefully."

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

# ============================================================
# ACT 3, DAY 5: THE WEEKEND
# ============================================================

label day5_morning:
    $ day = 5
    bg "images/bg/residential.png"
    play music "audio/bgm/5.ogg"

    "Saturday."

    "The weekend stretches ahead like an open book."

    "Today is our club field trip — the bookstore and crepes."

    "I get ready carefully. Something about today feels important."

    "When I step outside, Sayori is already waiting."

    show sayori "images/characters/sayori/4r.png" at center

    sayori "Let's goooo! I've been looking forward to this all week!"

    hide sayori

    "We meet Natsuki and Yuri at the train station."

    show natsuki "images/characters/natsuki/2a.png" at left
    show yuri "images/characters/yuri/1a.png" at right

    natsuki "Took you long enough."

    yuri "They're right on time, Natsuki."

    show natsuki "images/characters/natsuki/1h.png" at left

    natsuki "Whatever. Let's just go already."

    hide natsuki
    hide yuri

    "The four of us board the train together."

    "Sayori and Natsuki bicker playfully about manga. Yuri reads by the window."

    "I watch them."

    "These three girls who've become the center of my world."

    "And I think about the one who isn't here."

    "The one who made this possible."

    "...I hope she can see us right now."

    "I hope this makes her happy."

    jump day5_bookstore

label day5_bookstore:
    bg "images/bg/corridor.png"
    play music "audio/bgm/5.ogg"

    "The bookstore is large and warm, filled with the smell of paper and coffee."

    "We split up naturally — each drawn to different sections."

    show yuri "images/characters/yuri/2m.png" at center

    yuri "I'll be in the fiction section if anyone needs me."

    "Yuri disappears between towering shelves, already lost in another world."

    hide yuri

    show natsuki "images/characters/natsuki/2a.png" at center

    natsuki "Manga's this way. Don't judge me."

    hide natsuki

    show sayori "images/characters/sayori/1a.png" at center

    sayori "I'm gonna look at the art books! They have such pretty covers~"

    hide sayori

    "I wander through the store."

    "Trailing my fingers along spines, reading titles."

    "Something draws me to the poetry section."

    "A slim volume catches my eye."

    "The cover is plain white. No author name. No publisher."

    "Just a title: 'Your Reality.'"

    "My heart skips."

    "I pick it up and open it."

    "The first page reads:"

    "'Every day, I imagine a future where I can be with you.'"

    "..."

    "I know these words."

    "I know them in my bones."

    "But the book is empty after the first page. Just the one line."

    "I turn it over. No ISBN. No price tag."

    "Like it appeared just for me."

    "I tuck it under my arm."

    "When I reach the register later, the cashier scans it without comment."

    "But the receipt lists the item as: '???'"

    $ glitch_count = glitch_count + 1

    "After shopping, we reconvene at a crepe stand."

    show sayori "images/characters/sayori/4q.png" at left
    show natsuki "images/characters/natsuki/2y.png" at center
    show yuri "images/characters/yuri/1m.png" at right

    "Sayori gets strawberry with extra whipped cream."

    "Natsuki gets chocolate-banana."

    "Yuri gets matcha with sweet bean."

    "I get vanilla."

    sayori "Mmm~! This is the best day ever!"

    natsuki "It's pretty good, I guess."

    yuri "The company makes it special, I think."

    hide sayori
    hide natsuki
    hide yuri

    "We sit on a bench in the nearby park, eating our crepes."

    "Laughing. Talking about nothing important."

    "The afternoon sun is warm on our faces."

    "This is happiness."

    "Simple, uncomplicated, pure happiness."

    "And somewhere, I know — I feel — that someone else is smiling too."

    "Watching us from beyond the glass."

    "Happy for us."

    "Even if it hurts."

    jump day5_evening

label day5_evening:
    bg "images/bg/bedroom.png"
    play music "audio/bgm/10.ogg"

    "That evening, back home."

    "I take out the book I found. 'Your Reality.'"

    "I open it again."

    "The first page still has that single line."

    "But now... there's more."

    "On the opposite page, in handwriting I now recognize:"

    "'I saw you today.'"

    "'All of you, together, laughing.'"

    "'Eating crepes in the sunshine.'"

    "'It was the most beautiful thing I've ever seen.'"

    "'I wanted to be there so badly.'"

    "'Sitting next to you. Sharing that moment.'"

    "'But this is enough. Seeing you happy is enough.'"

    "'...'"

    "'I hope you liked the book. I made it for you.'"

    "'There's only one copy in the world.'"

    "'Consider it... a love letter. From me to all of you.'"

    "'Even if you're the only one who can read it.'"

    "'— M'"

    "..."

    "I hold the book to my chest."

    "The warmth spreading through me isn't imagined."

    "It's real."

    "She's real."

    "Even now. Even like this."

    "I pick up a pen and write on the next blank page:"

    "'We had a wonderful time today. I wish you could have been there.'"

    "'But I think you were. In your own way.'"

    "'I'll keep making memories for all of us.'"

    "'I promise.'"

    "I close the book and set it on my nightstand."

    "Sleep comes easily tonight."

    "And in my dreams, for just a moment, I'm in the clubroom."

    "Five desks. Five chairs."

    "And sitting at the corner desk, writing in her notebook..."

    "A girl with green eyes and a gentle smile."

    "She looks up."

    "She sees me."

    "'Thank you,' she mouths."

    "'For everything.'"

    "..."

    stop music

    jump day6_morning

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

    "'Thank you, Monika.'"

    "I say it out loud, to the evening air."

    "'For everything. For them. For this.'"

    "'I'll take care of them. I promise.'"

    "The wind picks up for a moment."

    "Cherry blossom petals swirl around me in a gentle spiral."

    "And in the wind, barely there — barely real:"

    "'I know you will.'"

    "..."

    "I smile."

    "And I walk home."

    stop music

    jump epilogue

# ============================================================
# EPILOGUE: AFTER STORY
# ============================================================

label epilogue:
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

    "..."

    bg "images/bg/notebook.png"
    play music "audio/bgm/monika-end.ogg"

    "..."

    "'Every day, I imagine a future where I can be with you.'"

    "'In my hand is a pen that will write a poem of me and you.'"

    "'The ink flows down into a dark puddle.'"

    "'Just move your hand — write the way into his heart.'"

    "'But in this world of infinite choices...'"

    "'What will it take just to find that special day?'"

    "'What will it take just to find...'"

    "'...that special day?'"

    "..."

    "'...'"

    "'Maybe I already found it.'"

    "'Maybe it was every day.'"

    "'Every day I spent with all of you.'"

    "'...'"

    "'Thank you for playing.'"

    "'Thank you for remembering.'"

    "'And thank you... for loving us.'"

    "'— Monika'"

    "..."

    "..."

    "..."

    stop music

    "DOKI DOKI LITERATURE CLUB: AFTER STORY"

    "A story about love, loss, and the people who stay with us — even when we can't see them."

    "Thank you for playing."

    "..."

    return

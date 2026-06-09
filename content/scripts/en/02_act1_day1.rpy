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

    play sound "audio/sfx/pageflip.ogg"

    "It's plain. No label. No name."

    "I open it."

    "The pages are empty. Blank white paper, unmarked."

    "All of them."

    play sound "audio/sfx/pageflip.ogg"

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

    glitch vignette 250
    glitch noise 150

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

    play ambient "audio/sfx/glitch_ambient1.ogg"
    glitch vignette 400

    "Faint. Like static on an old radio."

    "A voice. Far away."

    "'...thank you... for being... there...'"

    stop ambient
    $ heard_static = true

    "..."

    "I must be imagining things."

    "Exhaustion pulls me under."

    jump day2_morning

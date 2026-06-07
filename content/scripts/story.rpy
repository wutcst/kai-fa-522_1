# ================================================================
#  "Hoshimi Academy Love Comedy"
#  A Japanese-style school romcom visual novel
# ================================================================

# ----------------------------------------------------------------
#  PROLOGUE - First Day at Hoshimi Academy
# ----------------------------------------------------------------

label start:
    scene outside
    bg "images/bg_outside.png"
    "April."
    "Cherry blossom petals drift lazily from the canopy above..."
    "...painting the stone path to the school gate in soft pink."
    "This is Hoshimi Academy -- my new school as of today."
    "Transferring in the middle of spring semester is awkward enough."
    "But being late on your very first day? That takes a special kind of talent."
    "I check my phone. 8:27 AM. The ceremony starts at 8:30."
    "Three minutes. The gate is right there. I can make it."
    "In light novels, this is usually the part where the protagonist..."
    "...crashes into a girl at a corner and triggers some fateful encounter."
    "I glance around nervously. No corners in sight. Coast is clear."
    "Alright, time to sprint--"

    show kaede "images/char_kaede_normal.png" at center
    "A voice cuts through the morning air like a blade."
    "\"Halt.\""
    "I freeze mid-step and slowly turn around."
    "Long black hair cascades down like a waterfall."
    "A crimson ribbon flutters gently in the breeze."
    "Deep red eyes fix me with a gaze that could freeze lava."
    "On her left arm, a red armband reads: Student Council President."
    "...Oh no."

    kaede "You. You are the transfer student joining Class 2-A today, correct?"
    kaede "The opening ceremony begins at 8:30 sharp."
    kaede "It is now... 8:29."
    kaede "I suggest you run."

    "I don't need to be told twice."
    "\"Y-Yes ma'am!\""
    "I bolt through the gate at full speed, bag flapping behind me."
    "I can feel those red eyes boring into my back the entire way."
    "...And that's how I met Ichibano Kaede, Student Council President."
    "First impression: terrifying."
    "Second impression: ...actually, just terrifying."
    "But something tells me this won't be the last time we cross paths."

    $ met_kaede = true
    hide kaede

    "Somehow, I make it to the ceremony hall with seconds to spare."
    "The principal drones on about tradition and excellence."
    "I zone out, still catching my breath."
    "My chaotic new school life... begins now."

    jump day_loop

# ----------------------------------------------------------------
#  MAIN DAY LOOP
# ----------------------------------------------------------------

label day_loop:
    call show_location
    menu:
        "Look around":
            call look_around
            jump day_loop
        "Move":
            jump travel_menu
        "Talk to someone":
            call talk
            jump day_loop
        "End the day":
            jump end_day

label show_location:
    "[room_description()]"
    "Exits: [room_exits()]"
    return

# ----------------------------------------------------------------
#  LOOK AROUND - Environmental descriptions
# ----------------------------------------------------------------

label look_around:
    if current_room() == "outside":
        "The wrought-iron gate of Hoshimi Academy towers overhead."
        "Ivy crawls up the stone pillars, and beyond them stretches a tree-lined path."
        "Students mill about in groups, chatting and laughing."
        "The clock tower in the distance reads the current hour with quiet dignity."
        "A bulletin board near the gate is plastered with club recruitment posters."
        if day >= 3:
            "By now, a few students wave at me as they pass. I'm starting to fit in."
    if current_room() == "theater":
        "The massive lecture hall stretches upward in tiers of wooden seats."
        "Afternoon sunlight pours through the tall windows, catching dust motes."
        "The chalkboard at the front still has yesterday's equations scrawled across it."
        "The back rows are suspiciously comfortable -- perfect napping territory."
        if met_ruru:
            "I instinctively glance at the far corner of the last row."
    if current_room() == "pub":
        "Cafe Plume bathes everything in a warm amber glow."
        "The wooden counter is polished to a mirror sheen."
        "Mismatched mugs line the shelf behind the register."
        "Postcards and doodles from regular customers cover one entire wall."
        "The rich aroma of freshly ground coffee fills every corner."
        "A small chalkboard menu lists today's specials in elegant handwriting."
    if current_room() == "lab":
        "Rows of monitors glow with an ethereal blue light."
        "The air conditioning hums aggressively -- it's always freezing in here."
        "A whiteboard in the corner is covered in flowcharts and mysterious formulas."
        "Someone has left an empty energy drink can pyramid on one desk."
        "The clicking of keyboards creates a oddly rhythmic ambient soundtrack."
    if current_room() == "office":
        "The Student Council room is immaculate. Not a paper out of place."
        "A massive whiteboard dominates one wall, covered in schedules and plans."
        "Each task is color-coded and annotated in perfect handwriting."
        "By the window, a mug reads 'President Only' in bold letters."
        "There's a small vase of fresh flowers on the desk. A surprisingly soft touch."
        if kaede_affection >= 2:
            "I notice an extra chair has appeared at the side of the main desk."
            "Was that always there...?"
    return

# ----------------------------------------------------------------
#  TALK - Main conversation router
# ----------------------------------------------------------------

label talk:
    if current_room() == "outside":
        if met_kotori and day >= 3:
            call talk_kotori_outside
        elif met_kaede:
            call talk_kaede_gate
        else:
            "There's no one I know here right now."
            "Just students hurrying to their next destination."
    elif current_room() == "theater":
        if not met_ruru:
            call first_meet_ruru
        elif ruru_bug_event and not ruru_game_jam_event and day >= 4:
            call talk_ruru_game_jam
        else:
            call talk_ruru_theater
    elif current_room() == "pub":
        if not met_kotori:
            call first_meet_kotori
        elif kotori_lost_event and not kotori_poem_event and day >= 4:
            call talk_kotori_poem
        else:
            call talk_kotori_cafe
    elif current_room() == "lab":
        if met_ruru:
            call talk_ruru_lab
        else:
            "The computer room is mostly empty."
            "A few students are working on assignments, headphones on, worlds away."
    elif current_room() == "office":
        if met_kaede:
            if kaede_bento_event and not kaede_late_night_event and day >= 4:
                call talk_kaede_late_night
            else:
                call talk_kaede_office
        else:
            "The Student Council room is empty."
            "Every surface is organized with military precision."
            "Whoever runs this place clearly doesn't mess around."
    else:
        "There's nobody around to talk to."
    return

# ----------------------------------------------------------------
#  KAEDE ROUTE - Gate encounter
# ----------------------------------------------------------------

label talk_kaede_gate:
    show kaede "images/char_kaede_normal.png" at center
    "After classes end, I spot a familiar figure at the school gate."
    "The Student Council President stands by the pillar, clipboard in hand."
    "Her hair catches the afternoon light as she scans the departing crowd."

    kaede "...You again. I see you managed to not be late today."
    kaede "Don't misunderstand. I'm not waiting for anyone."
    kaede "I'm simply... monitoring the after-school traffic flow."

    menu:
        "Thanks for all your hard work, President.":
            kaede "...Hmph. It's my duty. I don't need your gratitude."
            show kaede "images/char_kaede_blush.png" at center
            kaede "...But."
            kaede "...Thank you. For noticing."
            "She turns away sharply, but not before I catch the tips of her ears turning red."
            "Like ripe strawberries. The comparison pops into my head unbidden."
            $ kaede_affection = kaede_affection + 1
        "Were you waiting for someone?":
            kaede "I just SAID I wasn't! Are your ears purely decorative?!"
            "She snaps her clipboard shut with a loud crack."
            "But I definitely saw it -- the page she was looking at was completely blank."
            "...Suspicious."
        "That clipboard is upside down, you know.":
            show kaede "images/char_kaede_blush.png" at center
            kaede "---!"
            "She fumbles the clipboard, nearly dropping it."
            kaede "I-It is NOT upside down! I was reading it perfectly fine!"
            "She flips it around. It was absolutely upside down."
            kaede "...This conversation never happened."
            "She marches off, ears blazing red."
            "I can't help but smile."
            $ kaede_affection = kaede_affection + 1

    hide kaede

    if not kaede_umbrella_event and day >= 2:
        "As I start walking home, I notice dark clouds gathering."
        "Did the forecast mention rain today...?"
        "I don't have an umbrella."
        show kaede "images/char_kaede_normal.png" at center
        "\"Here.\""
        "Something pokes me in the shoulder. I turn to find Kaede holding out a folding umbrella."
        kaede "The forecast said 70% chance of rain this afternoon."
        kaede "A responsible student checks the weather before leaving home."
        "\"But... what about you, President?\""
        kaede "I have a spare. Obviously. I always come prepared."
        show kaede "images/char_kaede_blush.png" at center
        kaede "Don't read anything into this. I simply can't have a student catching cold."
        kaede "It would reflect poorly on the Student Council."
        "She turns on her heel and walks away before I can respond."
        "The umbrella is light purple with tiny star patterns."
        "...Somehow, it doesn't seem like a 'spare.'"
        $ kaede_umbrella_event = true
        $ kaede_affection = kaede_affection + 1
        hide kaede

    return

# ----------------------------------------------------------------
#  KAEDE ROUTE - Student Council Room
# ----------------------------------------------------------------

label talk_kaede_office:
    bg "images/bg_office.png"
    show kaede "images/char_kaede_normal.png" at center
    "I push open the Student Council room door."

    kaede "Knock before entering. How many times must I say this?"
    "\"The door was open...\""
    kaede "...Sit down. Tea is on the shelf. Help yourself."
    "For someone so strict, she never actually turns me away."

    if not kaede_bento_event:
        "I notice a neatly wrapped bento box sitting at the corner of her desk."
        "The cloth wrapping has a subtle floral pattern. Very elegant."
        menu:
            "That bento looks amazing. Did you make it yourself?":
                show kaede "images/char_kaede_blush.png" at center
                kaede "---!"
                kaede "That-- I merely-- I accidentally made too much this morning!"
                kaede "It would be wasteful to throw it away, so I brought it!"
                kaede "It is absolutely NOT for you! Don't get the wrong idea!"
                kaede "............"
                kaede "...Do you want it?"
                "\"I would be honored.\""
                "She shoves the bento toward me without meeting my eyes."
                "Inside: perfectly arranged rice, tamagoyaki, grilled salmon, pickled vegetables."
                "Every piece is immaculate. This was clearly made with tremendous care."
                "\"This is incredible! President, you're an amazing cook!\""
                kaede "Naturally. A member of the Ichibano family excels at everything."
                "Despite her haughty words, she keeps glancing at me between bites."
                "When I finish every last grain of rice, I swear I see her smile."
                "Just for a second."
                $ kaede_bento_event = true
                $ kaede_affection = kaede_affection + 2
            "I'll let you eat in peace. Sorry for intruding.":
                kaede "...You don't have to leave."
                "Was that a hint of disappointment in her voice?"
                "Nah. Must be my imagination."
                kaede "...I mean, it makes no difference to me whether you stay or go."
                "She picks up her pen and returns to her paperwork."
                "But she doesn't actually write anything for a full minute."
    else:
        kaede "...I didn't bring a bento today. Stop looking at my desk like that."
        "\"I wasn't--\""
        show kaede "images/char_kaede_blush.png" at center
        kaede "Tomorrow... I might accidentally make too much again."
        kaede "Purely by coincidence. It has nothing to do with you."
        kaede "...Make sure you're here at lunch."
        "She buries her face in her paperwork."
        "I definitely don't imagine the small smile hidden behind those documents."
        $ kaede_affection = kaede_affection + 1

    hide kaede
    return

# ----------------------------------------------------------------
#  KAEDE ROUTE - Late Night Council Room
# ----------------------------------------------------------------

label talk_kaede_late_night:
    bg "images/bg_office.png"
    show kaede "images/char_kaede_normal.png" at center
    "It's already past 6 PM. Most students have gone home."
    "But light still spills from under the Student Council room door."
    "I peek inside. Kaede is hunched over her desk, surrounded by papers."

    "\"President? It's getting late...\""
    kaede "Hm? Oh. You're still here?"
    kaede "I'm fine. The cultural festival planning documents need to be finished tonight."
    "Her voice is steady, but there are shadows under her eyes."
    "An empty coffee cup sits beside three more crumpled ones."

    menu:
        "Let me help. Two people can finish faster.":
            kaede "You? Help? You don't even know the filing system."
            "\"Teach me then. I'm a quick learner.\""
            "She stares at me for a long moment, then sighs."
            kaede "...Fine. Sit there. I'll explain the format."
            "We work side by side for the next hour."
            "At first she corrects every tiny mistake I make."
            "But gradually, the corrections turn into quiet murmurs of approval."
            show kaede "images/char_kaede_blush.png" at center
            "When we finally finish, the sky outside is dark and full of stars."
            kaede "...You didn't have to stay."
            "\"I wanted to.\""
            kaede "...Idiot."
            "But she says it so softly, it almost sounds like something else entirely."
            $ kaede_late_night_event = true
            $ kaede_affection = kaede_affection + 2
        "You should take a break. You'll burn out at this rate.":
            kaede "The Ichibano family does not 'burn out.' We persevere."
            "\"Even the strongest sword breaks if you keep hammering it.\""
            "She pauses, pen hovering over paper."
            kaede "...That's surprisingly poetic coming from you."
            kaede "...Perhaps a five-minute break wouldn't be unreasonable."
            "She leans back in her chair and closes her eyes."
            "In the quiet room, with the sunset painting everything gold..."
            "She looks... fragile. Different from her usual iron composure."
            kaede "...Don't stare. It's impolite."
            "She didn't open her eyes. How did she know?"
            $ kaede_late_night_event = true
            $ kaede_affection = kaede_affection + 1

    hide kaede
    return

# ----------------------------------------------------------------
#  RURU ROUTE - First Meeting (Lecture Hall)
# ----------------------------------------------------------------

label first_meet_ruru:
    bg "images/bg_theater.png"
    "Lunch break. The lecture hall should be empty at this hour."
    "I figured it'd be a quiet place to eat my convenience store sandwich."
    "But there, in the very last row, in the furthest corner--"
    "A small figure is curled up like a cat in a sunbeam."

    show ruru "images/char_ruru_normal.png" at center
    "Purple hair. A black cat-ear headband. A lollipop dangling from her lips."
    "She's staring at a laptop screen, fingers flying across the keyboard."
    "The clacking echoes in the empty hall like rapid-fire gunshots."
    "She hasn't noticed me at all."

    "\"Um... hello?\""
    "No response. Not even a twitch."
    "\"...Hello?\""
    "Still nothing. I wave my hand in front of her face."

    show ruru "images/char_ruru_excited.png" at center
    ruru "---YESSS! IT COMPILED! ZERO ERRORS!"
    "She leaps from her seat, nearly launching her laptop into orbit."
    "Her arms shoot up in victory, lollipop flying across the room."
    "Then she freezes, finally registering my existence."

    show ruru "images/char_ruru_normal.png" at center
    ruru "..."
    ruru "........."
    ruru "...Who?"
    "\"I'm the new transfer student in Class 2-A...\""
    ruru "...Oh. An NPC."
    "\"I'm not an NPC!\""
    ruru "Do you have a name?"
    "I introduce myself."
    ruru "Mm. Registered. Saved to database."
    ruru "I'm Minazuki Ruru. Game Development Club. Sole member."
    ruru "...Nobody came to the recruitment session."
    ruru "So it's just me. A one-woman army."
    ruru "But that's fine. You can make a game solo. Probably. Maybe."
    "She tilts her head, studying me like I'm an interesting bug report."
    ruru "...You have a weird aura. Like a main character in a cheap dating sim."
    "\"I'll take that as a compliment...?\""
    ruru "It wasn't one. But it wasn't not one either."
    "She pops a new lollipop from her pocket and returns to her screen."
    "I have a feeling my life just got more complicated."

    $ met_ruru = true
    hide ruru
    return

# ----------------------------------------------------------------
#  RURU ROUTE - Computer Room
# ----------------------------------------------------------------

label talk_ruru_lab:
    bg "images/bg_lab.png"
    show ruru "images/char_ruru_normal.png" at center
    "In the computer room, Ruru has claimed two monitors for herself."
    "The left one displays dense code. The right shows a pixel-art game."
    "A small pile of candy wrappers surrounds her like a nest."

    ruru "Ah... you came."
    ruru "Sit. There's a chair. Don't touch the right keyboard. Tests are running."
    "I pull up a chair beside her."

    if not ruru_bug_event:
        ruru "...Actually. I have a problem."
        ruru "A bug. Two days. No progress. My sanity bar is critically low."
        ruru "Want to see?"
        menu:
            "Sure, let me take a look.":
                ruru "Here. The player character clips through walls on collision."
                "I lean in and scan the code. I don't know much about game dev, but..."
                "\"Wait -- this line. Shouldn't you check for collision BEFORE moving?\""
                show ruru "images/char_ruru_excited.png" at center
                ruru "!!!"
                ruru "You-- HOW-- Wait-- That's--"
                ruru "THAT'S IT! Two days! TWO DAYS! And you just--!"
                "Her fingers become a blur on the keyboard."
                "Two minutes of frantic typing later..."
                ruru "All green... ALL GREEN! Tests passed!"
                ruru "You... your INT stat must be maxed out."
                ruru "Or maybe mine was debuffed by sleep deprivation."
                ruru "Either way... join my party."
                "\"...Are you asking me to join the Game Dev Club?\""
                ruru "Affirmative. The flag has been triggered. No takebacks."
                ruru "...Also. Thank you."
                "That last part was barely a whisper. But I heard it."
                $ ruru_bug_event = true
                $ ruru_affection = ruru_affection + 2
            "I don't know much about programming, sorry...":
                ruru "...That's okay. Sit there anyway."
                ruru "Having someone nearby... Focus +20%. Probably thermal reasons."
                ruru "Human bodies generate heat. This room is cold. Simple physics."
                show ruru "images/char_ruru_normal.png" at center
                "She doesn't look at me, but her cat-ear headband seems to twitch."
                "Must be my imagination. Headbands can't move on their own."
                "...Right?"
                $ ruru_bug_event = true
                $ ruru_affection = ruru_affection + 1
    else:
        ruru "Progress today: good. All systems nominal."
        ruru "...Correlation with your presence: under investigation."
        "\"Is that your way of saying you're glad I'm here?\""
        show ruru "images/char_ruru_normal.png" at center
        ruru "...No comment. Pleading the fifth."
        ruru "...But if you left, the data would be incomplete."
        ruru "So stay. For science."
        $ ruru_affection = ruru_affection + 1

    hide ruru
    return

# ----------------------------------------------------------------
#  RURU ROUTE - Lecture Hall revisit
# ----------------------------------------------------------------

label talk_ruru_theater:
    bg "images/bg_theater.png"
    show ruru "images/char_ruru_normal.png" at center
    "Ruru is in her usual corner, but today she's eating a rice ball."
    "Make that three rice balls. The wrappers suggest a fourth existed."

    ruru "Lunch. Convenience store. 3-second unwrap time. Maximum efficiency."
    "\"You should eat something more nutritious...\""
    ruru "This has seaweed. Seaweed is a vegetable. Nutritional requirements: met."
    "That's... not how that works."

    if not ruru_lunch_event:
        menu:
            "What if I brought lunch for both of us tomorrow?":
                show ruru "images/char_ruru_excited.png" at center
                ruru "--! Really...?!"
                "Her eyes go wide, sparkling like twin monitors at full brightness."
                show ruru "images/char_ruru_normal.png" at center
                ruru "...I mean. If you insist. I won't refuse."
                ruru "Refusing would trigger a bad ending flag. I'm min-maxing outcomes."
                ruru "...It's not because I'm happy or anything."
                "Her ears are pink. Cat-ear headbands definitely cannot blush."
                "And yet."
                $ ruru_lunch_event = true
                $ ruru_affection = ruru_affection + 1
            "At least eat somewhere warmer. You'll get sick.":
                ruru "HP regeneration is not affected by ambient temperature."
                ruru "...But if you bring extra food sometime... I can help dispose of it."
                ruru "Waste reduction. Environmentally conscious."
                "She stuffs the last rice ball in her mouth to avoid saying more."
    else:
        "Today I brought enough for two. Sandwiches, fruit, juice boxes."
        "I set the spread between us."
        show ruru "images/char_ruru_excited.png" at center
        ruru "...!"
        "She reaches for a strawberry sandwich with the speed of a speedrun."
        show ruru "images/char_ruru_normal.png" at center
        ruru "...Not bad. This party's support class is top-tier."
        ruru "...Come back tomorrow. For continued data collection."
        $ ruru_affection = ruru_affection + 1

    hide ruru
    return

# ----------------------------------------------------------------
#  RURU ROUTE - Game Jam
# ----------------------------------------------------------------

label talk_ruru_game_jam:
    bg "images/bg_theater.png"
    show ruru "images/char_ruru_excited.png" at center
    "I find Ruru bouncing in her seat, which is extremely unusual."
    "Her normal state is 'statue with occasional keyboard inputs.'"

    ruru "Emergency quest! Critical priority!"
    ruru "There's a 48-hour game jam this weekend."
    ruru "Theme: 'Connection.' Deadline: Sunday midnight."
    ruru "I have the code. I have the engine. But..."
    show ruru "images/char_ruru_normal.png" at center
    ruru "...I can't draw. And I can't write stories."
    ruru "My pixel art looks like abstract nightmares."
    ruru "My dialogue reads like error logs."
    ruru "...I need a party member."
    "She looks up at me with those big violet eyes."
    "For the first time, she looks genuinely vulnerable."

    menu:
        "I'm in. Let's make a game together.":
            show ruru "images/char_ruru_excited.png" at center
            ruru "PARTY FORMATION CONFIRMED!"
            "She leaps up, grabbing both my hands without thinking."
            ruru "We'll meet Saturday morning! I'll bring the laptop! And snacks!"
            ruru "This is going to be the greatest game jam in history!"
            "She's gripping my hands tightly, face flushed with excitement."
            "Then she realizes what she's doing."
            show ruru "images/char_ruru_normal.png" at center
            ruru "...Ah."
            "She releases my hands like they're on fire."
            ruru "...Physical contact was unintended. Buffer overflow."
            ruru "...See you Saturday."
            "She pulls her hood over her head and dives behind her laptop screen."
            $ ruru_game_jam_event = true
            $ ruru_affection = ruru_affection + 2
        "I can try, but I've never made a game before.":
            ruru "Irrelevant. Passion > experience. That's in all the tutorials."
            ruru "Besides... you fixed my bug on day one."
            ruru "You have natural talent. Like finding a rare drop in a starter zone."
            "\"Is that a compliment?\""
            ruru "...Statement of fact. Not a compliment. Don't let it go to your head."
            ruru "...But yes."
            $ ruru_game_jam_event = true
            $ ruru_affection = ruru_affection + 1

    hide ruru
    return

# ----------------------------------------------------------------
#  KOTORI ROUTE - First Meeting (Cafe)
# ----------------------------------------------------------------

label first_meet_kotori:
    bg "images/bg_pub.png"
    "I push open the door to Cafe Plume."
    "A delicate chime rings overhead, announcing my arrival."
    "Warm light washes over me immediately -- golden, inviting, like a hug."
    "The scent of freshly ground coffee wraps around everything."

    show kotori "images/char_kotori_normal.png" at center
    "Behind the counter stands a young woman with honey-gold hair."
    "It's gathered in a loose braid over one shoulder, wisps framing her face."
    "She wears a coffee-brown apron over her school uniform."
    "When she notices me, she smiles -- slow and warm, like sunrise."

    kotori "Welcome to Cafe Plume."
    kotori "Table for one? There's a lovely spot by the window that just opened up."
    "\"Ah, yes, thank you...\""
    "I settle into the window seat. She drifts over unhurriedly."
    kotori "First time here, isn't it? I haven't seen your face before."
    kotori "And I know all our regulars by heart."
    "She taps her chin thoughtfully."
    kotori "Let me guess... transfer student?"
    "\"How did you know?!\""

    show kotori "images/char_kotori_laugh.png" at center
    kotori "Fufu... You hesitated at the door for about fifteen seconds before coming in."
    kotori "That kind of nervousness... it's like opening a new book."
    kotori "You're not sure what story awaits inside, but you're curious enough to turn the page."

    show kotori "images/char_kotori_normal.png" at center
    kotori "I'm Shiratori Kotori. Third-year. I also work here part-time."
    kotori "It's nice to meet you. I have a feeling we'll be seeing each other often."
    "She tilts her head slightly, that gentle smile never wavering."
    kotori "So -- what would you like to drink?"

    menu:
        "What do you recommend for a first-timer?":
            kotori "Hmm... for a first visit, I'd say hot cocoa."
            kotori "With just a pinch of cinnamon."
            kotori "It tastes like being wrapped in a blanket on an autumn evening."
            "\"That sounds perfect.\""
            kotori "Coming right up. Take your time -- this place is best enjoyed slowly."
            "She glides away, humming something soft and melodic."
            "The hot cocoa, when it arrives, is exactly as she described."
            "Warm. Gentle. Like the person who made it."
            $ kotori_affection = kotori_affection + 1
        "Just a regular latte, please.":
            kotori "Simple and classic. No sugar?"
            "\"No sugar.\""
            kotori "Straightforward... just like you."
            "She smiles and heads to the machine."
            "I'm not sure if that was a compliment or just an observation."
            "With her, it might be both."
        "Actually, surprise me.":
            show kotori "images/char_kotori_laugh.png" at center
            kotori "Oh my. A brave soul."
            kotori "Then I'll make something special. A Kotori original."
            "She disappears behind the counter, and I hear various bottles clinking."
            "What arrives is a pale lavender drink with a tiny star-shaped cookie on top."
            kotori "I call it 'First Chapter.' Because every first meeting deserves its own drink."
            "It tastes like flowers and vanilla, with a hint of something I can't name."
            "Something memorable."
            $ kotori_affection = kotori_affection + 2

    $ met_kotori = true
    hide kotori
    return

# ----------------------------------------------------------------
#  KOTORI ROUTE - Cafe revisit
# ----------------------------------------------------------------

label talk_kotori_cafe:
    bg "images/bg_pub.png"
    show kotori "images/char_kotori_normal.png" at center

    kotori "Welcome back. Your usual spot is open."
    "Without thinking, I head to the window seat. It's become 'my spot' already."

    if not kotori_lost_event:
        kotori "Actually... may I ask you something?"
        kotori "After my shift ends today, I need to pick up a book from the station bookstore."
        kotori "The problem is... last time I tried, I got lost for thirty minutes."
        "\"...The station is five minutes from here.\""
        show kotori "images/char_kotori_laugh.png" at center
        kotori "Yes, well... I saw a cat on the way, and then a interesting cloud, and then..."
        kotori "Before I knew it, I was at the river."
        show kotori "images/char_kotori_normal.png" at center
        kotori "So if you wouldn't mind being my guide...?"
        menu:
            "Of course. I'd be happy to help.":
                kotori "Wonderful. I knew I could count on you."
                kotori "It's strange... I've only known you a short while."
                kotori "But somehow, being around you feels like rereading a favorite book."
                kotori "Familiar. Comfortable."
                "She extends her pinky finger across the table."
                kotori "Pinky promise? You won't let me wander off?"
                "I hook my pinky with hers. Her hand is warm from holding coffee cups all day."
                "\"I promise. No detours.\""
                kotori "Hmm... maybe one small detour. If we see something interesting."
                "She smiles that slow, sun-warm smile."
                $ kotori_lost_event = true
                $ kotori_affection = kotori_affection + 2
            "Don't they have maps on your phone?":
                show kotori "images/char_kotori_laugh.png" at center
                kotori "I do use it! But I get... distracted."
                kotori "A flower here, a stray cat there, a beautiful shop window..."
                kotori "The world has too many interesting things. My feet follow my eyes."
                "\"That's... kind of endearing, actually.\""
                show kotori "images/char_kotori_normal.png" at center
                kotori "...Is it?"
                "She looks genuinely surprised. Then pleased."
                kotori "Most people just call it hopeless."
                $ kotori_lost_event = true
                $ kotori_affection = kotori_affection + 1
    else:
        kotori "I finished the book you helped me find."
        kotori "It was a short story collection. One story stood out to me..."
        kotori "About two people who meet by coincidence in spring."
        kotori "And how that one small moment... changes everything that follows."
        "She traces the rim of her coffee cup with one finger."
        kotori "Do you think meetings between people are coincidence? Or fate?"
        menu:
            "I think it's what we do after meeting that matters.":
                show kotori "images/char_kotori_normal.png" at center
                kotori "..."
                kotori "...That's a beautiful answer."
                kotori "Like something out of a novel."
                "She looks at me with those sky-blue eyes, and I forget to breathe for a second."
                $ kotori_affection = kotori_affection + 1
            "Fate, definitely.":
                show kotori "images/char_kotori_laugh.png" at center
                kotori "A romantic answer from an unexpected source."
                kotori "I'll write that down in my notebook. For future reference."
                "She pulls out her pocket notebook and actually writes something."
                "I'll never know what."
                $ kotori_affection = kotori_affection + 1

    hide kotori
    return

# ----------------------------------------------------------------
#  KOTORI ROUTE - Outside encounter
# ----------------------------------------------------------------

label talk_kotori_outside:
    bg "images/bg_outside.png"
    show kotori "images/char_kotori_normal.png" at center
    "After school, Kotori emerges from the gate carrying a stack of books."
    "The tower of volumes wobbles precariously with each step."

    kotori "Oh! Good timing."
    kotori "The weather is lovely today. Perfect for walking."
    kotori "Also perfect for reading. And for doing nothing at all."
    kotori "Every kind of day deserves appreciation, don't you think?"

    if not kotori_rain_event and day >= 5:
        "As if to mock her words, a fat raindrop splats on my nose."
        "Then another. And another."
        "Within seconds, it's a downpour."
        kotori "...Ah."
        "\"Quick, under the awning!\""
        "We dash to the nearest overhang, pressed close together to stay dry."
        "Her hair smells like coffee and old books."
        show kotori "images/char_kotori_laugh.png" at center
        kotori "Well... I did say every kind of day deserves appreciation."
        kotori "Even sudden rain."
        "\"Because it gives us an excuse to stand close together?\""
        show kotori "images/char_kotori_normal.png" at center
        kotori "..."
        "Did I just say that out loud? I definitely just said that out loud."
        kotori "...You're more bold than I expected."
        kotori "I was going to say 'because rain makes the world smell fresh.'"
        kotori "But... I like your answer better."
        "She doesn't move away."
        $ kotori_rain_event = true
        $ kotori_affection = kotori_affection + 2
        hide kotori
    else:
        menu:
            "Want to walk together for a bit?":
                kotori "I'd love that. You pick the direction today."
                kotori "If I choose, we'll end up at the ocean somehow."
                show kotori "images/char_kotori_laugh.png" at center
                kotori "Last time I tried to go to the convenience store, I reached the shrine on the hill."
                "\"...How?\""
                kotori "I followed a butterfly."
                "Incredible. Truly incredible."
                $ kotori_affection = kotori_affection + 1
            "Heading to the cafe today?":
                kotori "Not today. It's my day off."
                kotori "Days off are strange. So much freedom it becomes paralyzing."
                "She tilts her head like this is a genuine philosophical puzzle."
                kotori "Perhaps I'll sit somewhere and watch the clouds."
                kotori "Would you like to join me? Two people watching clouds is better than one."

        hide kotori
    return

# ----------------------------------------------------------------
#  KOTORI ROUTE - Poem Event
# ----------------------------------------------------------------

label talk_kotori_poem:
    bg "images/bg_pub.png"
    show kotori "images/char_kotori_normal.png" at center
    "Today, Kotori looks different. She's standing behind the counter, frowning at a notebook."
    "An actual frown. On Kotori. That's like seeing a cat bark."

    "\"Something wrong?\""
    kotori "Ah... it's embarrassing."
    kotori "I'm trying to write a poem for the literary magazine."
    kotori "But the words won't come out right."
    kotori "I know what I want to say. I just can't find the shape for it."

    menu:
        "What's the poem about?":
            kotori "...It's about spring. And new beginnings."
            kotori "And... finding warmth in unexpected places."
            "She looks at me as she says this. Holds the look a beat too long."
            show kotori "images/char_kotori_laugh.png" at center
            kotori "...I suppose my muse just walked in."
            "She writes something quickly, smiles, and snaps the notebook shut."
            kotori "Thank you. You always seem to help without even trying."
            $ kotori_poem_event = true
            $ kotori_affection = kotori_affection + 2
        "Would it help to read it out loud to someone?":
            kotori "...Would you listen?"
            "\"Of course.\""
            "She clears her throat softly and reads."
            "The poem is about a bird finding a branch to rest on after a long flight."
            "It's short. Simple. And somehow makes my chest feel tight."
            show kotori "images/char_kotori_normal.png" at center
            kotori "...Well?"
            "\"It's beautiful. Really.\""
            "She clutches the notebook to her chest, cheeks dusted pink."
            kotori "...Thank you. That means more than you know."
            $ kotori_poem_event = true
            $ kotori_affection = kotori_affection + 1

    hide kotori
    return

# ----------------------------------------------------------------
#  TRAVEL SYSTEM
# ----------------------------------------------------------------

label travel_menu:
    menu:
        "Go East":
            if can_go("east"):
                go east
                call on_enter_room
                jump day_loop
            else:
                "There's no path in that direction."
                jump travel_menu
        "Go South":
            if can_go("south"):
                go south
                call on_enter_room
                jump day_loop
            else:
                "There's no path in that direction."
                jump travel_menu
        "Go West":
            if can_go("west"):
                go west
                call on_enter_room
                jump day_loop
            else:
                "There's no path in that direction."
                jump travel_menu
        "Go North":
            if can_go("north"):
                go north
                call on_enter_room
                jump day_loop
            else:
                "There's no path in that direction."
                jump travel_menu
        "Stay here":
            jump day_loop

label on_enter_room:
    if current_room() == "outside":
        bg "images/bg_outside.png"
    if current_room() == "theater":
        bg "images/bg_theater.png"
        if not visited_theater:
            $ visited_theater = true
            "The lecture hall stretches out before me, vast and echoing."
            "Sunlight streams through tall windows, painting golden stripes across the seats."
            "It smells like chalk and old wood."
    if current_room() == "pub":
        bg "images/bg_pub.png"
        if not visited_pub:
            $ visited_pub = true
            "The cafe door chimes as I enter."
            "Immediately, the outside world feels far away."
            "Just warmth, coffee, and soft background music."
    if current_room() == "lab":
        bg "images/bg_lab.png"
        if not visited_lab:
            $ visited_lab = true
            "The computer room greets me with a wall of cold air."
            "Fluorescent lights buzz overhead."
            "It's the quietest place on campus -- perfect for focus."
    if current_room() == "office":
        bg "images/bg_office.png"
        if not visited_office:
            $ visited_office = true
            "The Student Council room is pristine."
            "A handwritten schedule on the door lists operating hours."
            "The penmanship is flawless. I can guess who wrote it."
    return

# ----------------------------------------------------------------
#  END OF DAY
# ----------------------------------------------------------------

label end_day:
    bg "images/bg_outside.png"
    "The sunset paints the school buildings in shades of amber and rose."
    "Another day at Hoshimi Academy draws to a close."

    if day == 1:
        "My first day... it was more eventful than I could have imagined."
        "A terrifying Student Council President. A mysterious computer room girl."
        "And somewhere nearby, a cafe that feels like it's been waiting for me."
        "Tomorrow, I'll explore more."

    if kaede_affection >= 3 and day >= 3:
        "...Was it my imagination, or was the President a bit less harsh today?"
        "No, that's definitely wishful thinking."
        "...But she did say 'see you tomorrow.' She's never said that before."

    if ruru_affection >= 3 and day >= 3:
        "My phone buzzes. A message from an unknown number."
        "\"Bug fixed. Your emotional support contributed approximately 47% to success.\""
        "\"...This is Ruru. I got your number from the class list. Don't ask how.\""
        "Followed by seventeen cat emojis."
        "I add the contact: 'Ruru (Game Dev Club).'"

    if kotori_affection >= 3 and day >= 3:
        "Walking past Cafe Plume, I see Kotori through the window wiping tables."
        "She catches my eye and waves -- a small, warm gesture."
        "Then she holds up her notebook and points at it, mouthing 'inspiration.'"
        "I'm not sure what that means. But it makes me smile."

    if day >= 5:
        "Five days at this school... and somehow it already feels like home."
        "These people -- Kaede, Ruru, Kotori -- they've each carved out a space."
        "A space in my daily life that I can't imagine being empty anymore."

    "Tomorrow will bring its own stories."
    "For now... good night, Hoshimi Academy."

    $ day = day + 1
    jump day_loop

# ----------------------------------------------------------------
#  END GAME (reserved)
# ----------------------------------------------------------------

label end_game:
    bg "images/bg_outside.png"
    "\"Hoshimi Academy Love Comedy\""
    "--- Demo End ---"
    "Thank you for playing."
    "The full story is still being written."
    "Until next time... may your days be full of unexpected encounters."
    return

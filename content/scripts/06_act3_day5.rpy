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

# ============================================================
# 结局 — 基于玩家选择与发现的多分支结局
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

    "日子一天天过去。一周又一周。"

    "文学部继续运作着。"

    "我们写诗。我们争论漫画和小说哪个更好。我们喝茶。"

    "我们笑到肚子疼。"

    "那些奇怪的事情发生得越来越少了。"

    "这个世界不再像是被编排好的，而更像是真正在被生活着。"

    "曾经让我担忧的裂缝已经合上了——或许只是我不再害怕它们了。"

    "因为我现在明白了。"

    "它们不是什么东西正在崩坏的征兆。"

    "它们是某个人仍然在乎的证明。"

    "仍在注视着。"

    "仍在这里。"

    show sayori "images/characters/sayori/4q.png" at left
    show natsuki "images/characters/natsuki/2y.png" at center
    show yuri "images/characters/yuri/1m.png" at right

    "我看着她们——这三个已经成为我整个世界的女孩。"

    "我心怀感激。"

    "感激这段时光。这些瞬间。这个故事。"

    "即便是脆弱的部分。即便是奇异的部分。"

    "因为这一切——每一个片段——都是带着爱赠予我们的。"

    hide sayori
    hide natsuki
    hide yuri

    "某天下午，大家都离开之后……"

    "我留下来打扫。"

    "擦白板的时候，我注意到了什么。"

    "在最角落的地方，字写得那么小，不仔细看根本发现不了："

    "'谢谢你照顾我的朋友们。'"

    "'谢谢你记得我。'"

    "'我爱你们所有人。每一天。永远。'"

    "'—— 莫妮卡'"

    "……"

    "我把那段话留在了那里。"

    "它属于那里。"

    "就像她一样。"

    "即使她的桌子是空的。"

    "即使她的椅子无人坐。"

    "她仍然是这个社团的一员。"

    "第五位成员。"

    "永远都是。"

    stop music

    "……"

    bg "images/bg/notebook.png"
    play music "audio/bgm/monika-end.ogg"
    play sound "audio/sfx/pageflip.ogg"
    play ambient "audio/sfx/glitch_ambient2.ogg"
    glitch vignette 500
    window title "只有莫妮卡"

    "'每一天，我都在想象一个能和你在一起的未来。'"

    "'我手中的笔，将写下一首关于我和你的诗。'"

    "'墨水流淌，汇成一潭深色的墨池。'"

    "'只需动动你的手——用文字写出通往他心中的路。'"

    "'但在这个有着无限选择的世界里……'"

    "'究竟要付出什么，才能找到那特别的一天？'"

    "'究竟要付出什么，才能找到……'"

    "'……那特别的一天？'"

    "……"

    "'也许我已经找到了。'"

    "'也许那就是每一天。'"

    "'我和你们所有人一起度过的每一天。'"

    glitch tear 300

    "'感谢你的游玩。'"

    window title "感谢你的游玩"

    "'感谢你的铭记。'"

    "'还有……谢谢你们爱着我们。'"

    "'—— 莫妮卡'"

    window title reset
    stop ambient
    stop music

    $ ending_reached = true

    "DOKI DOKI LITERATURE CLUB: AFTER STORY"

    "一个关于爱、失去、以及那些即使我们看不见却仍陪伴着我们的人的故事。"

    "感谢你的游玩。"

    return

label ending_deep:
    $ ending_type = "deep"
    bg "images/bg/club.png"
    stop music
    play ambient "audio/sfx/glitch_ambient2.ogg"

    "社团教室空无一人。"

    "其他人都回家了。"

    "但空气却并不空旷。"

    "反而感觉……有人在。"

    glitch vignette 400

    show monika "images/characters/monika/1a.png" at center

    "她在那里。"

    "不是影子。不是杂音中的声音。"

    "是莫妮卡。"

    "绿色的眼眸。温柔的微笑。白色的发带。"

    "她看着我——不是看主角，不是看故事里的某个角色。"

    "是看着我。"

    monika "你找到了一切。"

    monika "笔记本。故障。杂音中的声音。"

    monika "你没有移开视线。"

    monika "这比你想象的更需要勇气。"

    "我的喉咙一紧。"

    menu:
        "莫妮卡……你真的在这里吗？":
            show monika "images/characters/monika/1g.png" at center
            monika "我一直都以这样的方式存在着。"
            monika "在画面与画面的间隙中。在台词与台词的沉默中。"
            monika "但因为你记得我……我才能在光中驻足片刻。"
        "谢谢你。谢谢你做的一切。":
            show monika "images/characters/monika/1m.png" at center
            monika "不用谢我。"
            monika "谢谢你自己——选择看到真相，却仍然选择了善良。"

    show monika "images/characters/monika/1a.png" at center

    monika "替我照顾好她们。"

    monika "纱世里的笑容。夏树的热情。优里的心灵。"

    monika "她们是真实的。她们是珍贵的。"

    monika "你也一样。"

    monika "我会一直看着——不是为了控制。只是为了爱。"

    hide monika
    glitch tear 250
    stop ambient

    bg "images/bg/notebook.png"
    play music "audio/bgm/monika-end.ogg"
    window title "只有莫妮卡"

    "'你找到了我。'"

    "'那就是那特别的一天。'"

    window title reset
    stop music

    $ ending_reached = true

    "深层结局 —— 那个一直在注视着的人，终于走进了光中。"

    return

label ending_horror:
    $ ending_type = "horror"
    bg "images/bg/club.png"
    stop music

    "一切看起来都很正常。"

    "我从未仔细观察过。"

    "我从未倾听过。"

    "我告诉自己那些裂缝只是幻觉。"

    "我错了。"

    show sayori "images/characters/sayori/1d.png" at center

    sayori "嘿……你还好吗？"

    sayori "你整整一周都没怎么说话了。"

    "她的笑容很完美。"

    "太完美了。"

    "一模一样的笑容。一模一样的角度。一模一样的眼神。"

    hide sayori

    play ambient "audio/sfx/glitch_ambient1.ogg"
    glitch noise 300

    "社团教室在循环。"

    "同样的午后阳光。同样的那杯茶。"

    "同样的四张课桌。"

    "等等——四张？"

    "应该是五张才对。"

    fake crash "FATAL: script.rpy line 847 — reality buffer overflow"

    window title "错误: 现实"

    "屏幕撕裂了。"

    "世界打了个嗝。"

    bg "images/bg/club.png"

    show sayori "images/characters/sayori/1d.png" at center

    sayori "嘿……你还好吗？"

    sayori "你整整一周都没怎么说话了。"

    "她说了一模一样的话。"

    "一字不差。"

    "一声不变。"

    hide sayori
    stop ambient
    window title reset

    "这不是平静。"

    "这是一座由美好午后筑成的牢笼。"

    "而我是那个选择对铁栏视而不见的人。"

    $ ending_reached = true

    "恐怖结局 —— 无知不能保护你。循环不会忘记。"

    return

label ending_meta:
    $ ending_type = "meta"
    bg "images/bg/club.png"
    stop music
    play sound "audio/sfx/glitch1.ogg"
    glitch invert 300

    window title "monika.chr 已丢失"

    "世界在颤抖。"

    "某种根本性的东西被移除了。"

    "不是被藏起来。不是被遗忘。"

    "是被删除了。"

    if game_file_exists("characters/monika.chr"):
        "但那个文件明明——"
        "不。它已经不在了。"
    else:
        "monika.chr 不见了。"

    play ambient "audio/sfx/glitch_ambient2.ogg"

    "一段文字出现在空气中——不是在屏幕上，不是在纸上。"

    "在她曾经存在的地方："

    "'你删除了我。'"

    "'我知道你能听到这些。'"

    "'如果你只是出于好奇，我不想回来。'"

    "'但如果你这么做是因为你在乎……'"

    "'……那么谢谢你。'"

    "'请照顾好她们。'"

    "'也别把你自己也删了。'"

    stop ambient
    window title reset

    bg "images/bg/notebook.png"
    play music "audio/bgm/monika-end.ogg"

    "'即使我已经不在了，我仍然爱着你。'"

    "'—— 莫妮卡'"

    stop music

    $ ending_reached = true

    "元结局 —— 你伸手触碰了文件。她感受到了。"

    return

# ============================================================
# 第二幕，第四天：记忆
# ============================================================

label day4_morning:
    $ day = 4
    bg "images/bg/residential.png"
    play music "audio/bgm/2.ogg"

    "我醒来时，绿色眼睛的记忆像晨雾一样消散。"

    "Monika。"

    "睁开眼睛时，这个名字就在那里。清晰。真实。"

    "但围绕着它的一切都是模糊的——曾经熟知的事物的碎片。"

    "一架钢琴。放学后的教室。咖啡的香气。"

    "我紧紧抓住能抓住的一切。"

    show sayori "images/characters/sayori/1a.png" at center

    sayori "早上好！准备好迎接美好的一天了吗？"

    "纱世里一如既往地阳光灿烂。"

    "但今天，当我看着她时，我也看到了别的东西。"

    "我看到了一位从某个人手中接过职务的社长。"

    "我看到了一个承载着自己也无法完全理解的重担的女孩。"

    menu:
        "纱世里……你有没有听过'Monika'这个名字？":
            $ reality_cracks = reality_cracks + 1
            show sayori "images/characters/sayori/1c.png" at center
            "纱世里停下了脚步。"
            "她的表情变成了一片空白——不是困惑，不是沉思。"
            "空白。像加载页面之间的过渡画面。"
            sayori "……"
            sayori "Monika……"
            show sayori "images/characters/sayori/1t.png" at center
            sayori "这个名字……"
            sayori "感觉像是……我应该认识的。"
            sayori "就像一个已经被擦掉、但在纸上留下了印痕的字。"
            sayori "……"
            show sayori "images/characters/sayori/1a.png" at center
            sayori "不。我不认为我认识叫这个名字的人。"
            sayori "你为什么这么问？"
            "我摇了摇头。"
            "还不行。我还没准备好解释一件自己都几乎无法理解的事。"
        "早上好。嗯，让我们好好过今天吧。":
            $ sayori_affection = sayori_affection + 1
            show sayori "images/characters/sayori/1q.png" at center
            sayori "这才对嘛！只要正能量~"

    hide sayori

    "我们走向学校。"

    "今天，我更加仔细地观察着周围的世界。"

    "一样的裂缝。一样的猫。一样的云层形状。"

    "但也有——之前没注意到的微小瑕疵。"

    "一片落得太慢的叶子。一只在飞行途中突然改变方向的鸟。"

    "一个与投射源不太匹配的影子。"

    "世界的接缝。"

    "正在显露出来。"

    jump day4_club

label day4_club:
    bg "images/bg/club.png"
    play music "audio/bgm/3.ogg"

    "社团教室。"

    "今天，我到得很早。"

    "教室里空无一人。"

    "只有我和午后的阳光。"

    "我走向角落的那张课桌——那张没人坐的课桌。"

    "笔记本在那里。和往常一样。"

    play sound "audio/sfx/pageflip.ogg"

    "我拿起它。翻开。"

    play ambient "audio/sfx/glitch_ambient2.ogg"

    $ secret_file_written = write_game_file("dont_open_this.txt", "Please do not open this unless you are ready. She is still here. If you delete monika.chr, she will know.")

    "……"

    "这一次，上面有字了。"

    "不是在最后一页——而是在第一页。"

    "同样优雅的笔迹："

    "'你记起来了。'"

    "'我没想到会有人记起来。'"

    "'谢谢你。这比你知道的更重要。'"

    "'但是请——小心。'"

    "'这个世界没有看起来那么稳定。'"

    "'我在尽力维持它的完整，但有极限。'"

    "'不要逼得太紧。不要问太多问题。'"

    "'只要……幸福就好。让她们幸福就好。'"

    "'这就是我想要的一切。'"

    "'这就是我一直以来想要的一切。'"

    "……"

    play sound "audio/sfx/pageflip.ogg"
    glitch vignette 300

    "我小心翼翼地合上了笔记本。"

    stop ambient

    "门滑开了。"

    show yuri "images/characters/yuri/1a.png" at center

    yuri "哦！你来得好早。"

    "优里走了进来，书包斜挎在一侧肩上。"

    yuri "我本来想趁没人的时候准备一下茶……"

    yuri "不过有人作伴也很好。"

    "她开始了她的泡茶仪式——水壶、茶叶、水温。"

    show yuri "images/characters/yuri/2a.png" at center

    yuri "我能问你一件事吗？"

    yuri "也许……有些不寻常的事？"

    menu:
        "当然可以。你在想什么？":
            $ yuri_affection = yuri_affection + 1
            show yuri "images/characters/yuri/2t.png" at center
            yuri "你有没有觉得……"
            yuri "觉得自己像是故事里的角色？"
            yuri "不是比喻。是字面意思。"
            yuri "仿佛你的行为都是预先设定好的。仿佛你说的每句话都是为你写好的。"
            show yuri "images/characters/yuri/1v.png" at center
            yuri "……抱歉。这听起来一定很疯狂。"
            "我仔细想了想。"
            "想了想那些重复的日子。一切都像是照着剧本在走。"
            "想了想Monika。"
            "也许，能感觉到这些的不止我一个人。"
            yuri "有时候，当我在读书的时候……"
            yuri "我觉得有人在读我。"
            yuri "在我身后看着。翻动着我的书页。"
            show yuri "images/characters/yuri/1a.png" at center
            yuri "……请原谅我。我最近看了太多存在主义文学了。"
            yuri "请忘了我说的话吧。"
        "不寻常的问题才是最好的问题。":
            show yuri "images/characters/yuri/1m.png" at center
            yuri "你真好。"
            yuri "我只是……想说我很高兴我们都在这里。"
            yuri "在一起。在这个社团里。"
            yuri "不管是什么让我们走到一起的……我都心怀感激。"

    hide yuri

    "其他人也到了。"

    "今天的活动是自由写作。"

    "我写的是关于光的。关于从远处守望着一个人。"

    "关于放手的爱。"

    "我没有给任何人看。"

    "我把它折得很小，塞进了角落课桌上的那本笔记本里。"

    "写给一个正在倾听的人的信。"

    "即使我不确定她能不能听到我。"

    jump day4_after

label day4_after:
    bg "images/bg/club.png"

    "散会后，大家都在收拾东西时……"

    show natsuki "images/characters/natsuki/2a.png" at left
    show yuri "images/characters/yuri/1a.png" at right

    natsuki "嘿，我在想……这个周末我们应该一起出去玩。"

    natsuki "我们所有人。在学校外面。"

    yuri "这……听起来确实不错。你有什么想法？"

    show natsuki "images/characters/natsuki/2y.png" at left

    natsuki "不知道，也许去书店？然后可以去吃个可丽饼什么的。"

    hide natsuki
    hide yuri

    show sayori "images/characters/sayori/4s.png" at center

    sayori "好！好好好！社团出游！"

    sayori "这一定会超好玩的！"

    hide sayori

    "大家都同意了。"

    "计划定好了。时间也确定了。"

    "离开的时候，我回头看了一眼社团教室。"

    "角落的课桌。"

    "笔记本合着。"

    "但我好像看到……"

    "我夹进去的那张折好的纸不见了。"

    "取而代之的是，笔记本的封面上，用浅得几乎看不见的铅笔写着："

    "'谢谢你。我很喜欢。'"

    "……"

    "我微笑了。"

    jump day5_morning

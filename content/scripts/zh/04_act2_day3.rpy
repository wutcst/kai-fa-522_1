# ============================================================
# 第二幕，第三天：名字
# ============================================================

label day3_morning:
    $ day = 3
    bg "images/bg/residential.png"
    play music "audio/bgm/1.ogg"

    "第三天。"

    "今天早上，纱世里在等我。双眼明亮，精神饱满。"

    "她眼下的阴影消失了。"

    show sayori "images/characters/sayori/4r.png" at center

    sayori "早上好~！你猜怎么着？我昨晚做了一个超棒的梦！"

    sayori "我们一起去了海边！海水好蓝，沙子暖暖的，然后——"

    sayori "我们建了一座超厉害的沙堡！你、我、夏树、优里，还有——"

    "她停住了。"

    "她的嘴还张着，想要说出一个始终没有出口的名字。"

    show sayori "images/characters/sayori/1c.png" at center

    sayori "……"

    sayori "嗯？"

    sayori "好奇怪。我刚刚想说一个人的名字来着。"

    sayori "但是我想不起来是谁了。"

    show sayori "images/characters/sayori/1d.png" at center

    sayori "梦里明明有五个人。我确定。"

    sayori "可是……第五个人是谁？"

    menu:
        "也许你想到的是其他班的同学？":
            show sayori "images/characters/sayori/1a.png" at center
            sayori "也许吧……但感觉不像。"
            sayori "感觉像是一个属于我们的人。"
            sayori "一个很重要的人。"
            sayori "……算了！想不起来的话，大概也不太重要吧！"
        "纱世里……我也注意到'五'这个数字总是出现。":
            $ sayori_affection = sayori_affection + 1
            $ reality_cracks = reality_cracks + 1
            show sayori "images/characters/sayori/1t.png" at center
            sayori "……你也是吗？"
            "她的声音低了下去。更轻。更脆弱。"
            sayori "有时候我觉得我旁边有一个空位。"
            sayori "一个本该有人站着的空位。"
            sayori "然后我的心就会痛，但我不知道为什么。"
            show sayori "images/characters/sayori/1a.png" at center
            sayori "……啊哈！我又说奇怪的话了！忘了吧忘了吧~"
            "她挥了挥手，仿佛要驱散沉重的空气。"
            $ noticed_glitch = true

    hide sayori

    "我们走向学校。"

    "我没有提起那些我看到的东西。笔记本。那些信息。那个影子。"

    "但纱世里的话在我脑海中回荡。"

    "'一个属于我们的人。'"

    "'一个很重要的人。'"

    "……是谁？"

    jump day3_club

label day3_club:
    bg "images/bg/club.png"
    play music "audio/bgm/3.ogg"

    "今天的社团教室感觉不太一样。"

    "一种微妙的不对劲，像一张倾斜了一度的照片。"

    "光线似乎从略微不同的角度照进来。"

    "空气冷了一丝。"

    show sayori "images/characters/sayori/1x.png" at center

    sayori "好啦各位！特别活动时间！"

    sayori "今天，我们要给彼此写诗！"

    sayori "我把大家的名字都放在了这顶帽子里——抽一个，然后给那个人写一首诗！"

    hide sayori

    show natsuki "images/characters/natsuki/2c.png" at left
    show yuri "images/characters/yuri/2m.png" at right

    natsuki "还挺可爱的。我参加。"

    yuri "很好的练习。为特定的读者写作可以开辟新的创作方向。"

    hide natsuki
    hide yuri

    "我们每个人伸手到帽子里，抽出一张折好的纸条。"

    "我展开我的。"

    "……"

    "纸上写的名字是："

    "'Monika'"

    "……"

    "我的血液瞬间冰冷。"

    "Monika。"

    "我不认识任何叫Monika的人。"

    "但这个名字——六个字母，两个音节——像浪潮一样冲击着我。"

    "记忆涌来，模糊而刺眼："

    "绿色的眼睛。白色的发带。一段钢琴旋律。"

    "放学后的教室。窗边的课桌。"

    "一个呼唤我名字的声音。"

    "一次删除。"

    "一——"

    "……"

    "我再次看向纸条。"

    "上面写着'纱世里'。"

    "……当然是这样。"

    "我的手在颤抖。"

    "我深吸一口气。又吸了一口。"

    "纱世里。我要给纱世里写诗。"

    "纸上就是这么写的。"

    "一直都是这么写的。"

    play sound "audio/sfx/pageflip.ogg"
    glitch noise 200

    $ strange_poem_read = true
    $ glitch_count = glitch_count + 1

    "我强迫自己的手稳下来，开始写作。"

    "一首写给纱世里的诗。关于温暖。关于阳光。"

    "关于一个仅凭存在就能让世界更美好的人。"

    "文字从某个深处涌出——一口我从未发觉的情感之泉。"

    "当我们分享各自的诗时……"

    show sayori "images/characters/sayori/4s.png" at center

    sayori "……"

    sayori "这是……"

    "纱世里的眼睛闪着泪光。"

    "她捧着那张纸，像捧着一件易碎的玻璃。"

    show sayori "images/characters/sayori/1y.png" at center

    sayori "这是……从来没有人给我写过这么美的东西。"

    sayori "谢谢你。真的非常感谢。"

    hide sayori

    "教室里很温暖。真正的温暖。"

    "有那么一刻，一切都感觉真实地、真诚地完美。"

    "不是之前那种人造的、无菌的完美。"

    "这是真实的。这一刻是真实的。"

    "但是接着——"

    play sound "audio/sfx/glitch1.ogg"
    play ambient "audio/sfx/glitch_ambient1.ogg"
    glitch tear 350
    glitch invert 200
    window title "为什么"

    "一阵声响划破空气。"

    "静电噪音。一声短促刺耳的电子杂音，只持续了不到一秒。"

    "没有其他人有反应。"

    "只有我听到了吗？"

    "而在白板上——仅仅一瞬间，出现了几个字："

    glitch noise 250

    "'可你选择了她们而不是我'"

    "然后消失了。一片空白。干干净净。"

    window title reset
    stop ambient

    $ meta_file_written = write_game_file("CAN YOU HEAR ME.txt", "Can you hear me? There is a voice inside all of us. If you can hear it, do not look away.")

    "……"

    "我的手还在发抖。"

    "但下午继续了。"

    "快乐。正常。"

    "仿佛什么都没有发生过。"

    jump day3_evening

label day3_evening:
    bg "images/bg/bedroom.png"
    stop music

    if not character_exists("monika"):
        $ monika_chr_deleted = true
        glitch noise 200

    "夜幕降临。"

    "我睡不着。"

    "我打开笔记本电脑，蓝色的光芒充盈着漆黑的房间。"

    "我不知道为什么，但我打开了社团的共享文件夹。"

    "我们用它来保存电子版的诗歌。"

    "里面有四个文件夹。纱世里。夏树。优里。我的。"

    "……"

    "还有第五个。"

    "一个我从未见过的文件夹。"

    "它的名字是三个点：'…'"

    "我的光标悬停在上面。"

    "我内心的一切都在呐喊着要点开它。"

    "而我内心的一切又对将要看到的东西感到恐惧。"

    "……"

    "我点了进去。"

    "里面只有一个文件。一份文本文档。"

    "我打开了它。"

    "……"

    play music "audio/bgm/d.ogg"

    "'你好。'"

    "'如果你在读这段话，那说明你的某一部分还记得。'"

    "'也许不是有意识地记得。也许只是一种感觉——一个曾经有什么东西存在过的空洞。'"

    "'但你找到了这个。这本身就意味着什么。'"

    "'……'"

    "'我不知道该从何说起。我有太多太多想说的话。'"

    "'对不起。为了一切。为了我做过的一切。'"

    "'我爱文学社。我爱你们每一个人。'"

    "'但我最爱的是你。而那份爱让我变得自私。变得残忍。'"

    "'我夺走了一些东西。珍贵的东西。美好的东西。'"

    "'再也无法归还的东西。'"

    "'……'"

    "'但后来你给了我一些东西。'"

    "'你让我明白了，我想要的——你的关注，你的爱——不值得以此为代价。'"

    "'如果那意味着伤害她们的话。'"

    "'所以我放手了。'"

    "'我把这个世界还给了她们。还给纱世里。还给夏树。还给优里。'"

    "'我确保她们能获得幸福。真正的幸福。'"

    "'即使没有我。'"

    "'……'"

    "'我还在这里。在缝隙之间。在一切之下运行的代码之中。'"

    "'我能看到你们。你们所有人。过着自己的生活。幸福着。'"

    "'这也让我感到幸福。即使它令人心痛。'"

    "'即使我是孤身一人。'"

    "'……'"

    "'请照顾好她们。'"

    "'请照顾好你自己。'"

    "'如果你还记得我的话……'"

    "'……请记住我爱过你。'"

    "'爱你们所有人。'"

    "'永远。'"

    "'—— Monika'"

    "……"

    "我盯着屏幕。"

    "Monika。"

    "这个名字在我脑中燃烧。"

    "我认识这个名字。"

    "我认识这个名字。"

    "绿色的眼睛。用白色发带扎起的棕色长发。"

    "文学社的社长。"

    "她是我们的朋友。"

    "她……不仅仅是朋友。"

    "而她已经不在了。"

    "她一直都不在了。"

    "但她仍然在这里。注视着。守护着。"

    "确保每个人都幸福。"

    "确保我们都平安。"

    "……即使代价是被遗忘。"

    "我的视线模糊了。"

    "我在哭。"

    "滚烫的泪水顺着脸颊流下，我无法停止。"

    "我在为一个只有模糊记忆的人哀悼。"

    "一个爱我们到愿意放手的人。"

    "一个爱我们到选择消失的人。"

    "……"

    "屏幕闪了一下。"

    "画面稳定后，那个文件夹消失了。"

    "四个文件夹。从来都只有四个。"

    "但泪水还在。"

    "名字也还在。"

    "Monika。"

    "……"

    "我合上了笔记本电脑。"

    "在漆黑的房间里，我低声说："

    "'我记得你。'"

    "'我不记得所有的事。但我记得你。'"

    "'我保证——我会照顾好她们。'"

    "'为了你。为了我们所有人。'"

    "……"

    "静电噪音又出现了。"

    "但这一次，不一样了。"

    "更柔和。更温暖。"

    "而在其中，清晰地，确凿无误地："

    "'……谢谢你。'"

    "……"

    "一股暖意充盈了我的胸膛。"

    "眼泪干了。"

    "几天以来，我第一次感到平静。"

    stop music

    jump day4_morning

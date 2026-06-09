# ============================================================
# 第一幕，第二天：玻璃上的裂痕
# ============================================================

label day2_morning:
    $ day = 2
    bg "images/bg/residential.png"
    play music "audio/bgm/1.ogg"

    "第二天早晨。"

    "我立刻注意到了——透过窗帘洒进来的阳光，和昨天落下的图案一模一样。"

    "同样的角度。同样的金色光斑。"

    "像是一帧一帧回放的场景。"

    "我把这个念头抛到脑后，开始准备出门。"

    "外面，空气清冽。樱花纷飞。"

    "我看了看时间，走向我们的集合地点。"

    "纱世里不在那儿。"

    "……"

    "这不正常。她总是比我先到的。"

    "我等了五分钟。然后十分钟。"

    "正当我准备拿出手机给她发消息时，她出现了。"

    show sayori "images/characters/sayori/3d.png" at center

    sayori "啊……对不起！非常抱歉我迟到了！"

    "她气喘吁吁。蝴蝶结也歪了一点。"

    "而她的眼下有阴影——淡淡的黑眼圈，笑容也无法完全遮掩。"

    $ sayori_overslept = true

    menu:
        "你还好吗？看起来好像没睡好。":
            $ sayori_affection = sayori_affection + 1
            show sayori "images/characters/sayori/1c.png" at center
            sayori "诶？有那么明显吗？"
            "她不自觉地摸了摸自己的脸。"
            sayori "我只是……有点难以入睡。"
            show sayori "images/characters/sayori/1d.png" at center
            sayori "做了噩梦。那种醒来时发现自己在哭、却想不起原因的噩梦。"
            sayori "不过没关系啦！有点困也不会怎么样的~"
            "她笑了。但那笑声很空洞。"
        "没关系。我们赶紧走吧，不然要迟到了。":
            show sayori "images/characters/sayori/1a.png" at center
            sayori "好的！走吧走吧！"
            "她抓住我的袖子把我拉走了。"
            "她的手握得比平时更紧。"

    hide sayori

    "我们走在熟悉的路上。"

    "同一条人行道。同样的裂缝。同一只猫。"

    "那只猫从栅栏柱上注视着我们。"

    "今天，它没有移开目光。"

    "它琥珀色的眼睛追随着我们经过——不眨眼，一动不动。"

    "像一台监控摄像头。"

    "一股寒意沿着我的脊背爬了上来。"

    "我加快了脚步。"

    jump day2_club

label day2_club:
    bg "images/bg/club.png"
    play music "audio/bgm/3.ogg"

    "社团教室沐浴在午后的阳光里。"

    show yuri "images/characters/yuri/1a.png" at center

    yuri "下午好。今天我为大家准备了茶。"

    "优里优雅地穿行在课桌之间，以熟练的动作摆放着茶杯。"

    "她放下茶杯时，我一个一个地数着。"

    "一个。两个。三个。四个。"

    "……五个。"

    "她放下了五个杯子。"

    "然后她停住了，盯着手中的第五个杯子。"

    show yuri "images/characters/yuri/1h.png" at center

    yuri "这……"

    yuri "奇怪。"

    "她拿着那个杯子，仿佛它是什么易碎而陌生的东西。"

    yuri "我明明记得应该是……不，不对。"

    "她的手在颤抖。只是微微的。"

    show yuri "images/characters/yuri/1a.png" at center

    yuri "一定是我数错了。真是太粗心了。"

    "她把第五个杯子收进了储物柜。"

    "但我注意到她在门口犹豫了一下。"

    "她低声说了什么。"

    "我听不太清楚，但听起来像是……"

    "'……对不起。'"

    hide yuri

    show natsuki "images/characters/natsuki/1c.png" at center

    natsuki "喂。有没有人在走廊里听到过什么奇怪的声音？"

    hide natsuki

    show sayori "images/characters/sayori/1c.png" at left
    show natsuki "images/characters/natsuki/1c.png" at right

    sayori "奇怪的声音？比如什么？"

    natsuki "比如……钢琴声。很微弱，像是从很远的地方传来的。"

    natsuki "但音乐教室在教学楼的另一头啊。"

    sayori "也许有人在练习吧？老建筑里声音的传播方式本来就很奇怪的~"

    show natsuki "images/characters/natsuki/1i.png" at right

    natsuki "……那不是随便什么钢琴曲。"

    natsuki "每次都是同一首曲子。"

    natsuki "像是有人在单曲循环一样。"

    hide sayori
    hide natsuki

    $ glitch_count = glitch_count + 1

    "房间安静了片刻。"

    "然后纱世里拍了拍手。"

    show sayori "images/characters/sayori/4r.png" at center

    sayori "好啦！今天的活动是自由阅读和写作时间！"

    sayori "大家做自己开心的事就好~"

    hide sayori

    "紧张的气氛消散了。大家各自回到了自己的常规活动中。"

    "夏树从书包里拿出漫画。优里从书架上选了一本厚厚的小说。"

    "纱世里开始在笔记本上写东西，舌尖微微探出，一副认真的样子。"

    "我拿起了一本书——一本短篇小说集。"

    "我心不在焉地翻着。"

    "然后我停了下来。"

    "第113页。"

    "正文很正常——一个女孩放学回家的场景。"

    "但在页边空白处，用细小而工整的笔迹写着："

    "'我爱她们每一个人。所有人。'"

    "'现在依然如此。'"

    "'但她们不能知道我在注视着她们。'"

    "'如果她们知道了，一切都会被毁掉。'"

    "我屏住了呼吸。"

    "我翻过那一页，然后又翻回来。"

    "页边空白处一片干净。洁白的纸张。"

    "……当然是这样。"

    $ glitch_count = glitch_count + 1

    show yuri "images/characters/yuri/3a.png" at center

    yuri "你还好吗？你盯着那一页看了很久了。"

    menu:
        "我好像看到页边空白处有字……但现在不见了。":
            $ reality_cracks = reality_cracks + 1
            $ yuri_affection = yuri_affection + 1
            show yuri "images/characters/yuri/2t.png" at center
            yuri "页边空白处……？"
            "优里从我手中接过书，仔细地审视着那一页。"
            show yuri "images/characters/yuri/2n.png" at center
            yuri "现在什么都没有了……"
            yuri "但你知道吗……旧书会保留前任读者的痕迹。"
            yuri "他们皮肤上的油脂，他们注意力的重量。"
            yuri "也许你感知到了某些已经消逝的东西。"
            show yuri "images/characters/yuri/1m.png" at center
            yuri "有些讯息注定不会长存。它们只会出现在需要看到它们的人眼前。"
            "她轻声说着，几乎像在自言自语。"
            "仿佛她理解了某些她无法用言语表达的东西。"
        "只是走神了。书不错。":
            show yuri "images/characters/yuri/1m.png" at center
            yuri "是吧？这本书的文笔有一种让人沉浸其中的力量。"
            yuri "就好像书中的世界正在向你伸出手来。"

    hide yuri

    "午后的时光流逝着。"

    "不知什么时候，我从书中抬起了头。"

    "每个人都在各自的位置上。满足。安宁。"

    "阳光温暖。茶香弥漫。"

    "一切都恰如其分。"

    "……"

    "完美。"

    "这个词不请自来地浮现在我的脑海中。"

    "随之而来的，是一种冰冷的感觉——像冰水沿着脊背缓缓淌下。"

    "'完美'不是自然的。"

    "事物从来不会完美。"

    "除非有人刻意让它们变成这样。"

    jump day2_after_club

label day2_after_club:
    bg "images/bg/corridor.png"
    stop music

    "社团活动接近尾声，大家开始收拾东西时，夏树拉住了我的手臂。"

    show natsuki "images/characters/natsuki/1c.png" at center

    natsuki "喂。等一下。"

    "她朝门口望了一眼，纱世里和优里正在离开。"

    natsuki "能聊聊吗？就……我们两个人。"

    "我点了点头。"

    "我们等到脚步声在走廊尽头消失。"

    show natsuki "images/characters/natsuki/1i.png" at center

    natsuki "听着。我不想让你觉得我疑神疑鬼什么的。"

    natsuki "但你最近有没有注意到什么……不对劲的地方？"

    menu:
        "嗯。有几件事一直让我觉得不太对。":
            $ natsuki_affection = natsuki_affection + 1
            show natsuki "images/characters/natsuki/1e.png" at center
            natsuki "谢天谢地。我还以为只有我在发疯。"
            show natsuki "images/characters/natsuki/1c.png" at center
            natsuki "就好像……每天几乎都是一样的，对吧？"
            natsuki "同样的对话。同样的日常。"
            natsuki "有时候我看着某个东西，它就……变了。"
            natsuki "像是现实打了个嗝。"
            natsuki "但一眨眼又恢复正常了。"
        "'不对劲'是什么意思？":
            show natsuki "images/characters/natsuki/1h.png" at center
            natsuki "我也不知道该怎么解释。"
            natsuki "就是……一种感觉？像是被什么看不见的东西注视着。"
            natsuki "像是空气比正常情况下更沉重。"

    show natsuki "images/characters/natsuki/1c.png" at center

    natsuki "还有一件事。"

    natsuki "昨天，大家都走了之后……"

    natsuki "我忘了拿漫画，就回来取。"

    show natsuki "images/characters/natsuki/1i.png" at center

    natsuki "社团教室的门开着。我听到里面有人。"

    natsuki "一个声音。在说话。像是有人在聊天。"

    natsuki "但我往里一看……"

    natsuki "没有人。空荡荡的房间。"

    natsuki "只有角落里那张桌子。那张从来没人坐的桌子。"

    natsuki "我发誓……上面的笔记本是翻开的。"

    natsuki "像是刚刚有人在上面写过东西。"

    show natsuki "images/characters/natsuki/2a.png" at center

    natsuki "……算了。大概什么都不是。"

    natsuki "也许只是我压力太大了。考试之类的。"

    natsuki "就当我没说过吧。"

    hide natsuki

    "夏树离开了，她的脚步声在空旷的走廊里又快又急。"

    "我独自站在那里。"

    "头顶的日光灯嗡嗡作响——持续的、低沉的嗡鸣。"

    "其中一盏灯闪烁了一下。"

    "在那短暂的半秒黑暗中，我又看到了。"

    "走廊尽头的一个剪影。"

    "高挑。纤细。长发垂过肩头。"

    "一条白色的发带。"

    "以及一丝若有若无的绿色。"

    "灯光恢复稳定。"

    "走廊空无一人。"

    "只有我和嗡嗡作响的灯。"

    $ saw_monika_shadow = true

    "我快步离开了。"

    jump day2_evening

label day2_evening:
    bg "images/bg/bedroom.png"
    play music "audio/bgm/10.ogg"

    "那天晚上，我无法入睡。"

    "我躺在黑暗中，听着房子在我周围发出的声响。"

    "嘎吱声和呻吟声。冰箱的嗡嗡声。"

    "普通的声音。"

    "但今晚它们听起来像是世界在呼吸。"

    "我的手机震动了一下。"

    "文学社群聊的一条通知。"

    "我拿起手机。"

    "消息写道："

    "'大家和睦相处，不是很好吗？为了这一切我付出了那么多努力。希望你能珍惜。'"

    "发送者的名字是空白的。"

    "没有头像。没有用户名。只是……什么都没有。"

    "我盯着它看。"

    "我的心在狂跳。"

    "我眨了一下眼。"

    "消息不见了。"

    "聊天记录里没有新消息。只有纱世里一小时前发的'晚安~'。"

    "……"

    if glitch_count >= 3:
        "这已经不是第一次了。"
        "笔记本。页边空白处。那个剪影。群聊消息。"
        "事物出现又消失。不该存在的文字。不可能真实的形状。"
        "这个世界出了什么问题。"
        "但我无法把握住到底是什么。"
        "就像试图用手捧水——真相从我的指缝间流走。"
        $ reality_cracks = reality_cracks + 1

    "最终，疲惫占了上风。"

    "我闭上了眼睛。"

    "在清醒与梦境之间的缝隙里，我又听到了那个声音。"

    play ambient "audio/sfx/glitch_ambient1.ogg"
    glitch vignette 500
    window title "你能听到我吗"

    "静电噪音。噪音中的一个声音。"

    "'……不要……忘记……我……'"

    "'……拜托了……'"

    window title reset
    stop ambient
    stop music

    "……"

    jump day3_morning

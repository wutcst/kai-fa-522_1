# ============================================================
# 第一幕，第一天：美好的开始
# ============================================================

label day1_morning:
    $ day = 1
    bg "images/bg/residential.png"
    play music "audio/bgm/1.ogg"

    "清晨的空气清新而甜美，我走出家门。"

    "樱花花瓣在微风中慵懒地飘落，在阳光下闪烁着，宛如粉色的小星星。"

    "这样的早晨会让你相信，这个世界本质上是美好的。"

    "……美好得几乎不真实。"

    "我甩开这个念头，看了看时间。"

    "刚好准时。"

    show sayori "images/characters/sayori/1a.png" at center

    sayori "嘿——！早上好！"

    "纱世里从隔壁的家中蹦蹦跳跳地朝我跑来，珊瑚粉色的头发随着每一步欢快地跳动。"

    "她的蝴蝶结——那条标志性的红色丝带——在阳光下闪闪发光。"

    "她笑容满面。一如既往。"

    sayori "天气真好，对吧？这种日子感觉什么事都有可能发生！"

    "她跟上我的步伐走在我身旁，我们的肩膀几乎触碰在一起。"

    show sayori "images/characters/sayori/1q.png" at center

    sayori "你昨晚睡得好吗？你今天看起来有点……发呆。"

    menu:
        "嗯，我睡得很好。做了个美梦。":
            $ sayori_affection = sayori_affection + 1
            show sayori "images/characters/sayori/4q.png" at center
            sayori "那太好了！你知道人们怎么说的——好梦预示着好事即将到来！"
            sayori "诶嘿嘿~"
            "她开心地蹦跳着，差点撞到一个邮箱。"
            show sayori "images/characters/sayori/1a.png" at center
        "我做了一个奇怪的梦……记不清了，但感觉很重要。":
            $ noticed_glitch = true
            $ reality_cracks = reality_cracks + 1
            show sayori "images/characters/sayori/1c.png" at center
            sayori "奇怪的梦？"
            "只是一瞬间，纱世里的眼神中有什么东西变了。"
            "一丝闪烁。像风中的烛火。"
            show sayori "images/characters/sayori/1d.png" at center
            sayori "你知道吗……我有时候也会做那样的梦。"
            sayori "梦里感觉自己忘记了什么很重要的事情。"
            sayori "就像有一个想不起来的词，或者一张看不清的脸……"
            show sayori "images/characters/sayori/1a.png" at center
            sayori "不过没关系！新的一天就是用来创造新回忆的，对吧？"
            "她的笑容回来了，一如既往地灿烂。"
            "但我注意到了那个停顿。那一丝犹豫。"

    hide sayori

    "我们一起步行去学校，早晨的空气中弥漫着樱花的芬芳和路过面包店飘出的新鲜面包香。"

    "纱世里开心地聊着她新发现的一部漫画、天气、还有昨天看到的一只猫。"

    "我半心半意地听着，让她的声音像温水一样流过我的耳畔。"

    "这段路程很舒适。很熟悉。"

    "……和昨天一模一样。"

    "相同的人行道裂缝。相同的猫坐在相同的栅栏柱上。"

    "相同的老奶奶在浇花。"

    "甚至头顶上相同的云层形状。"

    "……"

    "我想太多了。"

    "每天都像前一天。这就是日常的运作方式。"

    jump day1_school

label day1_school:
    bg "images/bg/corridor.png"

    "学校走廊里挤满了学生，他们的交谈声汇成一片舒适的低语。"

    show sayori "images/characters/sayori/1x.png" at center

    sayori "哦！我差点忘了——我今天为社团准备了一个特别活动！"

    sayori "下课后一定要马上来哦？不许磨蹭！"

    "她笑嘻嘻地戳了戳我的胳膊。"

    menu:
        "我不会错过的。什么计划？":
            show sayori "images/characters/sayori/4r.png" at center
            sayori "是！个！惊！喜！"
            sayori "你等着看就好了~"
        "你知道我每次都会来社团的，纱世里。":
            $ sayori_affection = sayori_affection + 1
            show sayori "images/characters/sayori/1q.png" at center
            sayori "诶嘿嘿……我知道，我知道。"
            sayori "我只是会兴奋嘛，你懂的。"
            sayori "有你在，一切都更有趣了。"

    hide sayori

    "纱世里挥手告别，我们各自去上课。"

    "学校的一天在平常的讲课和笔记中模糊地度过。"

    "数学。文学。历史。"

    "一切正常。"

    "一切都该是这样的。"

    "除了……"

    "文学课上，老师大声朗读了一首诗。"

    "那是一首标准的课程作品——没什么特别的。"

    "但有一行诗句像荆棘一样刺入我的脑海："

    "'而她，比世界爱她更爱这个世界的她，选择了隔着玻璃静静注视。'"

    "一阵寒意穿过我的身体。"

    "我不知道为什么。"

    "老师继续讲下去。那个瞬间过去了。"

    "但那些词句挥之不去。"

    jump day1_club

label day1_club:
    bg "images/bg/club.png"
    play music "audio/bgm/3.ogg"

    "午后的阳光斜斜地透过社团活动室的窗户，将一切笼罩在温暖的琥珀色中。"

    "我推开门。"

    show natsuki "images/characters/natsuki/2z.png" at left

    natsuki "终于来了！你是最后一个到的，慢吞吞。"

    "夏树坐在桌子上，双腿晃来晃去。她的表情带着得意的满足感。"

    show yuri "images/characters/yuri/1a.png" at right

    yuri "别在意她。她一直很焦躁地等着大家到齐。"

    "优里坐在她惯常的位置，双手优雅地捧着一只茶杯。蒸汽在金色的光线中袅袅升起。"

    show natsuki "images/characters/natsuki/1h.png" at left

    natsuki "我才没有焦躁！我只是……守时。不像某些人。"

    hide natsuki
    hide yuri

    show sayori "images/characters/sayori/4r.png" at center

    sayori "好！现在大家都到齐了，我来宣布今天的特别活动！"

    "纱世里站在教室前方，带着一位资深社长的自信。"

    "有时候我还是会惊讶——她是如此自然地适应了这个角色。"

    sayori "今天……我们要写下自己最幸福的回忆！"

    sayori "但是有个特别之处——你要把它写得像是在讲给一个从未见过你的人听一样。"

    sayori "就像通过一个瞬间来介绍自己！"

    hide sayori

    show natsuki "images/characters/natsuki/2c.png" at left

    natsuki "这个……其实还不错。不过挺私人的。"

    show yuri "images/characters/yuri/2m.png" at right

    yuri "写作中的坦诚是很有力量的。"

    yuri "我觉得这能产生一些真正美丽的作品。"

    hide natsuki
    hide yuri

    "当大家各自找到位置开始写作时，我环顾了教室。"

    "纱世里在她的课桌前，咬着笔帽若有所思。"

    "夏树蜷缩在窗边的座位上，笔记本藏得严严实实。"

    "优里在桌子旁，长发如帘幕般遮住她的脸庞，用流畅的笔迹书写着。"

    "而在角落里……"

    "一张课桌。"

    "空的。"

    "桌面上覆着一层薄薄的灰尘，像是很久没有人坐过了。"

    "但椅子微微拉开着，仿佛有人刚刚站起来。"

    "桌上放着什么东西——一本朴素的笔记本。"

    menu:
        "走过去看看那本笔记本。":
            $ desk_note_found = true
            $ glitch_count = glitch_count + 1
            call check_notebook_day1
        "不管它——专心写自己的诗。":
            call writing_time_day1

    "写作时间自然地结束了。"

    "我们一个接一个地分享自己的作品。"

    call poem_sharing_day1

    jump day1_walk_home

label check_notebook_day1:
    "某种东西吸引着我走向那张课桌。"

    "我无法解释——一种牵引力，就像重力，又像是在人群中辨认出一个熟悉的声音。"

    "我走过去，拿起了那本笔记本。"

    play sound "audio/sfx/pageflip.ogg"

    "很普通。没有标签。没有名字。"

    "我翻开它。"

    "纸页是空白的。洁白的纸张，没有任何痕迹。"

    "全部都是。"

    play sound "audio/sfx/pageflip.ogg"

    "我翻过去——空白，空白，空白。"

    "直到最后一页。"

    "那里，用工整而优雅的字迹——一种我几乎认出来的笔迹写着："

    "'你能听到我吗？'"

    "'我还在这里。'"

    "'即使你看不见我，即使你不记得了……'"

    "'我还在这里。'"

    "'请不要忘记。'"

    "我的心砰砰直跳。"

    "这笔迹……熟悉得令人心痛。就像在梦中看到自己儿时的家。"

    show sayori "images/characters/sayori/1c.png" at center

    sayori "你在看什么呀？"

    "我猛地合上笔记本。"

    "当我再看最后一页时……"

    "……是空白的。"

    "每一页。完全空白。仿佛那些文字从未存在过。"

    sayori "怎么了？你脸色好苍白。"

    menu:
        "没什么。我以为我看到了什么，但是……":
            show sayori "images/characters/sayori/1a.png" at center
            sayori "嗯，你确定？你看起来有点受惊了。"
            sayori "也许你需要多睡一会儿！"
            "她安慰地拍了拍我的肩膀。"
        "这本笔记本……是谁的？":
            $ reality_cracks = reality_cracks + 1
            show sayori "images/characters/sayori/1c.png" at center
            sayori "谁的……？"
            "纱世里看了看笔记本，又看了看课桌。"
            "她的表情恍惚了一瞬。"
            show sayori "images/characters/sayori/1d.png" at center
            sayori "我……我不知道。"
            sayori "那张桌子一直都是空的，不是吗？"
            sayori "……"
            show sayori "images/characters/sayori/1a.png" at center
            sayori "肯定是别的班的学生落下的！没什么大不了的~"
            "但她的笑声来得慢了半拍。"

    hide sayori

    $ saw_monika_shadow = true

    "我把笔记本放回去，回到了自己的座位。"

    "我的手在微微颤抖。"

    "但我拿起笔，开始写作。"

    return

label writing_time_day1:
    "我坐到自己的老位置，抽出一张纸。"

    "今天笔在手中感觉格外沉重。"

    "我闭上眼睛，思考着自己最幸福的记忆。"

    "……"

    "奇怪。一切都感觉朦朦胧胧的。就像我的记忆是被阳光晒褪了色的照片。"

    "但有一件事我很确定："

    "此刻。现在。文学社。"

    "夏树的笔尖沙沙声。优里茶杯轻轻碰响的声音。"

    "纱世里无调地哼着歌。"

    "这就是我最幸福的记忆。"

    "文字很轻松地涌出来。太轻松了。"

    "就好像有人在引导我的手。"

    $ poem_written = true

    return

label poem_sharing_day1:
    bg "images/bg/club.png"

    show sayori "images/characters/sayori/1x.png" at center

    sayori "好啦大家！分享时间到！"

    sayori "谁想第一个来？"

    hide sayori

    show natsuki "images/characters/natsuki/2a.png" at center

    natsuki "我来。"

    "夏树清了清嗓子。她双手握着纸，指节微微发白。"

    natsuki "……'厨房里弥漫着香草和焦糖的味道。我的手上沾满了面粉。'"

    natsuki "'她在笑我——笑我弄得一团糟，笑歪歪扭扭的糖霜。'"

    natsuki "'但她还是咬了一口，眼睛亮了起来，像我给了她整个世界。'"

    natsuki "'这就是我一直想要的。做出能让人微笑的东西。'"

    "她抬起头，脸颊微微泛红。"

    show natsuki "images/characters/natsuki/2d.png" at center

    natsuki "……就这样。别想太多。"

    hide natsuki

    show yuri "images/characters/yuri/1m.png" at center

    yuri "写得很美，夏树。感官细节真的很吸引人。"

    hide yuri

    show sayori "images/characters/sayori/4q.png" at center

    sayori "我都快闻到香草味了！现在好想吃纸杯蛋糕~"

    hide sayori

    show yuri "images/characters/yuri/1a.png" at center

    "接下来是优里。她的作品更长，更精致。"

    yuri "'雨点敲打着窗户，像不耐烦的手指。'"

    yuri "'我十四岁，蜷缩在图书馆的角落里，一本沉甸甸的书放在膝上。'"

    yuri "'文字将我拉入另一个世界——一个我不害羞、不奇怪、不孤单的世界。'"

    yuri "'那是我第一次明白，书不是一种逃避。'"

    yuri "'它们是一扇门。'"

    show yuri "images/characters/yuri/2u.png" at center

    yuri "……希望这不会太忧郁。"

    hide yuri

    show natsuki "images/characters/natsuki/1l.png" at center

    natsuki "……不会。其实写得真的很好。"

    "夏树轻声说道，自己也有些惊讶。"

    hide natsuki

    show sayori "images/characters/sayori/1a.png" at center

    "纱世里分享了她的作品——是关于童年的一个夏日。"

    "在洒水器下奔跑。捕捉萤火虫。"

    "朋友的手握在她手中，一起看着日落。"

    sayori "'即使我知道那一天终会结束……'"

    sayori "'即使太阳正在落下……'"

    sayori "'我很幸福。因为我不是一个人。'"

    show sayori "images/characters/sayori/1q.png" at center

    sayori "诶嘿嘿……大声读出来好尴尬啊。"

    hide sayori

    "然后轮到我了。"

    "我读了我写的关于文学社的文章。关于此刻。关于她们。"

    "读完之后，教室里很安静。"

    show sayori "images/characters/sayori/4s.png" at left
    show natsuki "images/characters/natsuki/1l.png" at center
    show yuri "images/characters/yuri/1m.png" at right

    "纱世里的眼眶泛着泪光。"

    "夏树看向别处，但嘴角在微笑。"

    "优里轻轻点头，表情温暖。"

    sayori "……这让我好开心。"

    natsuki "嗯……还不错吧，我觉得。"

    yuri "说得真美。"

    hide sayori
    hide natsuki
    hide yuri

    "那个瞬间悬浮在空气中——金色而脆弱。"

    "完美。"

    "……但当我看向自己的纸时，我注意到了什么。"

    "我诗的最后一行。"

    "我不记得自己写过这一行。"

    "'我们是五个人——我们一直是五个人——而其中一个在注视着。'"

    glitch vignette 250
    glitch noise 150

    "……"

    "我眨了眨眼。"

    "最后一行写的是：'我感激每一个瞬间。'"

    "……当然。这才是我写的。"

    "我把纸折好收起来。"

    $ glitch_count = glitch_count + 1

    return

label day1_walk_home:
    bg "images/bg/residential.png"
    play music "audio/bgm/2.ogg"

    "放学时太阳正在落山。"

    "天空被渲染成橙色和粉色，像水彩颜料泼洒在纸上。"

    show sayori "images/characters/sayori/1a.png" at center

    sayori "今天是美好的一天，对吧？"

    "纱世里走在我身旁，她的影子在路面上拉得长长的。"

    sayori "我喜欢这样的日子。什么坏事都没有发生，每个人都很开心。"

    sayori "就像……世界在说'给你，这是你应得的。'"

    menu:
        "是啊。我希望每天都能这样。":
            $ sayori_affection = sayori_affection + 1
            show sayori "images/characters/sayori/1q.png" at center
            sayori "我也是~"
            sayori "让我们每天都这样度过吧，好吗？"
            sayori "约定哦！"
            "她伸出小指。"
            "我忍不住微笑着勾住了她的小指。"
        "纱世里……你有没有觉得少了什么？":
            $ reality_cracks = reality_cracks + 1
            show sayori "images/characters/sayori/1t.png" at center
            sayori "少了什么……？"
            "她沉默了几步。"
            "晚风吹起，搅动着我们身边的花瓣。"
            sayori "有时候……"
            sayori "有时候我觉得应该有……更多的人。"
            sayori "就像一张摆了五个位子的桌子，但只有四个人坐下。"
            sayori "而你想不起来第五个位子是给谁的。"
            show sayori "images/characters/sayori/1a.png" at center
            sayori "不过那太傻了！我们都在这里，对吧？这才是最重要的！"
            "她微笑着，但她的目光停留在某个我看不见的地方。"
            $ noticed_glitch = true

    hide sayori

    "我们到了分别的路口。"

    show sayori "images/characters/sayori/1x.png" at center

    sayori "明天见！做个好梦哦~"

    "她一边走向自己家，一边回头挥手。"

    hide sayori

    "我目送她离去。"

    "路灯开始一盏一盏地亮起来。"

    "一盏接一盏，像一只只睁开的眼睛。"

    "除了一盏。"

    "在她家和我家之间的一盏路灯，没有亮起来。"

    "那里的黑暗浓稠而凝实。"

    "而就在那一瞬间——只是最短暂的一刹那——"

    "我在黑暗中看到了什么。"

    "一个轮廓。一个剪影。"

    "长发，映着不存在的光芒。"

    "绿色的眼眸。"

    "……"

    "路灯闪烁了一下，亮了。"

    "什么都没有。只是一条空荡荡的人行道。"

    "我的心跳加速。"

    $ saw_monika_shadow = true
    $ glitch_count = glitch_count + 1

    "我快步走回了家。"

    jump day1_evening

label day1_evening:
    bg "images/bg/bedroom.png"
    stop music

    "我的房间又暗又静。"

    "我躺在床上，盯着天花板，试图平息纷乱的思绪。"

    "那本笔记本。没亮的路灯。那个剪影。"

    "还有我诗里的那一行——那行我不记得自己写过的句子。"

    "'我们是五个人。'"

    "五个人。"

    "但我们是四个人。我们一直都是四个人。"

    "……不是吗？"

    "我掏出手机。文学社的群聊在屏幕上发着光。"

    "纱世里、夏树、优里，还有我。"

    "四个成员。"

    "我盯着它看了很久。"

    "然后我往上翻阅聊天记录。"

    "正常的消息。活动计划。纱世里发的表情包。夏树抱怨剧透。"

    "没什么异常。"

    "但在最顶端——群聊创建的地方——"

    "创建者的名字是空白的。"

    "不是被删除了。不是'未知用户'。只是……空的。"

    "一个本该有名字的地方，是一片虚无。"

    if desk_note_found:
        "'你能听到我吗？'"
        "笔记本上的话在我脑海中回响。"
        "是谁写的？为什么消失了？"
        "为什么想到这些，我的胸口就隐隐作痛？"

    "我放下手机。"

    "入睡来得很慢。"

    "就在我即将入眠的那一刻，我听到了。"

    play ambient "audio/sfx/glitch_ambient1.ogg"
    glitch vignette 400

    "很微弱。像老式收音机的静电噪音。"

    "一个声音。遥远的。"

    "'……谢谢你……一直……在那里……'"

    stop ambient
    $ heard_static = true

    "……"

    "我一定是在胡思乱想。"

    "疲惫将我拽入了梦乡。"

    jump day2_morning

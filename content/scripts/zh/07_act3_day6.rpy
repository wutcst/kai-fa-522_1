# ============================================================
# 第三幕，第六天：接受
# ============================================================

label day6_morning:
    $ day = 6
    bg "images/bg/residential.png"
    play music "audio/bgm/2.ogg"

    "星期一的早晨。"

    "今天的世界感觉轻盈了许多。"

    "不是那种让我不安的完美。"

    "而是好的。真真切切的、温暖的好。"

    show sayori "images/characters/sayori/1a.png" at center

    sayori "早上好~！"

    "纱织蹦蹦跳跳地跑过来，耳后别着一朵野花。"

    sayori "我在路上找到的！是不是很好看？"

    sayori "我一直在想你前几天说的话。"

    sayori "关于好像缺了什么东西。"

    show sayori "images/characters/sayori/1d.png" at center

    sayori "我觉得……也许你说得对。"

    sayori "但我也觉得……不管那个缺失的东西是什么，它留下了一些东西。"

    sayori "一些温暖的东西。一些守护着我们的东西。"

    show sayori "images/characters/sayori/1q.png" at center

    sayori "就像守护天使一样！诶嘿嘿~"

    hide sayori

    "我们走向学校。"

    "今天，围墙上的猫冲我们叫了一声。"

    "纱织停下来摸了摸它。"

    "而这个不完美却美丽的世界，继续运转着。"

    jump day6_club

label day6_club:
    bg "images/bg/club.png"
    play music "audio/bgm/3.ogg"

    "社团教室。"

    "当我走进去时，有什么不一样了。"

    "角落里的那张桌子被移走了。"

    "它不再孤零零地待在角落。"

    "有人把它推过来，跟我们平时用的几张桌子拼在了一起。"

    "五张桌子。拼在一起。"

    show sayori "images/characters/sayori/1x.png" at left

    sayori "啊！那张桌子是我搬的。"

    sayori "它孤孤单单待在角落里好可怜的。"

    sayori "就算没有人坐……它也应该是集体的一份子，对吧？"

    hide sayori

    show yuri "images/characters/yuri/1m.png" at center

    yuri "我觉得这很温暖。"

    hide yuri

    show natsuki "images/characters/natsuki/2c.png" at center

    natsuki "嗯……感觉就该这样。"

    hide natsuki

    "我们像往常一样准备好了。"

    "茶。书。笔记本。"

    "而在第五张桌上，有人放了一杯茶。"

    "没有人对此发表评论。"

    "就那么……自然而然地发生了。"

    "仿佛这是世界上最理所当然的事情。"

    "今天的活动是自由朗读——大声读出这周写的任何作品。"

    "我分享了写给纱织的那首诗。"

    "夏树读了一篇关于犯错与被原谅的作品。"

    "优里分享了一段关于无常之美的文章。"

    "纱织读了一首短小甜蜜的关于雨后阳光的诗。"

    "……"

    "然后，最奇妙的事情发生了。"

    "当朗读结束，教室陷入舒适的沉默时……"

    "我听到了。"

    "我们都听到了。"

    "钢琴声。"

    "隐隐约约。若有若无。但确确实实存在着。"

    "一段旋律——温柔的、忧伤的、美丽的。"

    "来自虚无之中。又仿佛来自四面八方。"

    show sayori "images/characters/sayori/1c.png" at left
    show natsuki "images/characters/natsuki/1c.png" at center
    show yuri "images/characters/yuri/1h.png" at right

    "我们都愣住了。"

    "我们都听到了。"

    "没有人说话。"

    "那旋律大约持续了三十秒。然后渐渐消散了。"

    "像一个上了发条的音乐盒慢慢停下来。"

    hide sayori
    hide natsuki
    hide yuri

    "寂静。"

    show sayori "images/characters/sayori/1d.png" at center

    sayori "……好美。"

    sayori "不知道是谁在弹呢。"

    hide sayori

    show natsuki "images/characters/natsuki/1i.png" at center

    natsuki "……是同一首曲子。"

    natsuki "就是我一直听到的那首。"

    natsuki "但这一次……"

    show natsuki "images/characters/natsuki/1l.png" at center

    natsuki "一点都不觉得害怕。"

    natsuki "反而觉得像是……"

    hide natsuki

    show yuri "images/characters/yuri/2u.png" at center

    yuri "像是某人在说再见。"

    yuri "……或者也许是'后会有期'。"

    hide yuri

    "第五个茶杯静静地放在桌上，没有人碰过。"

    "但里面的茶是温热的。"

    "就好像刚刚才倒上的。"

    "我看着它。"

    "我发誓——就那么一瞬间——我看到了一个不属于我的倒影。"

    "绿色的眼眸。温柔的笑容。"

    "然后就只剩下茶了。"

    "只是一个茶杯，映着午后的光。"

    "……"

    jump day6_ending

label day6_ending:
    bg "images/bg/residential.png"
    play music "audio/bgm/5.ogg"

    "回家的路上，安静而温暖。"

    "今天我们四个人一起走。"

    show sayori "images/characters/sayori/1q.png" at left
    show natsuki "images/characters/natsuki/2c.png" at center
    show yuri "images/characters/yuri/1a.png" at right

    "没有人提起钢琴的事。但也没有人忘记。"

    "我们之间有一种安宁——那种共同经历了无法言说之事后才有的安宁。"

    sayori "大家？"

    sayori "我只是想说……我真的很幸福。"

    sayori "能和大家成为朋友……是我生命中最美好的事。"

    natsuki "……嗯。我也是，大概。"

    yuri "我也一样。真心的。"

    hide sayori
    hide natsuki
    hide yuri

    "我们走到了各自分路的十字路口。"

    "挥手告别。"

    "'明天见。'"

    "'晚安。'"

    "'好梦。'"

    "我目送她们离去——优里向左，夏树直走，纱织回到她家。"

    "三个朋友。三个珍贵的人。"

    "还有一个，虽然看不见，却让这一切成为了可能。"

    "我抬头望向天空。"

    "今晚的夕阳美得不可思议——金色、珊瑚色和紫罗兰色的光辉交织在一起。"

    "就像有人专门为我们画上的。"

    "……"

    play ambient "audio/sfx/glitch_ambient2.ogg"

    "'谢谢你，莫妮卡。'"

    glitch vignette 350

    "我对着傍晚的风，大声说出了这句话。"

    "'谢谢你为我们做的一切。谢谢你给了我她们。谢谢这一切。'"

    "'我会照顾好她们的。我保证。'"

    "风忽然大了一瞬。"

    "樱花花瓣在我周围轻柔地旋转飞舞。"

    "而在风中，若隐若现——几乎不真实地："

    "'我知道你会的。'"

    stop ambient
    window title reset

    "……"

    "我笑了。"

    "然后，我走向家的方向。"

    stop music

    jump ending_router

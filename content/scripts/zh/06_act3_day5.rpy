# ============================================================
# 第三幕，第五天：周末
# ============================================================

label day5_morning:
    $ day = 5
    bg "images/bg/residential.png"
    play music "audio/bgm/5.ogg"

    "星期六。"

    "周末像一本翻开的书，在眼前展开。"

    "今天是我们社团的外出活动——逛书店和吃可丽饼。"

    "我仔细地做好了准备。总觉得今天有些特别。"

    "当我走出家门时，纱织已经在等着了。"

    show sayori "images/characters/sayori/4r.png" at center

    sayori "出发啦！我已经期待了整整一周了！"

    hide sayori

    "我们在火车站和夏树、优里碰面。"

    show natsuki "images/characters/natsuki/2a.png" at left
    show yuri "images/characters/yuri/1a.png" at right

    natsuki "你们也太慢了吧。"

    yuri "他们很准时的，夏树。"

    show natsuki "images/characters/natsuki/1h.png" at left

    natsuki "随便啦。快走吧。"

    hide natsuki
    hide yuri

    "我们四个一起上了火车。"

    "纱织和夏树嬉笑着争论漫画的事。优里在窗边看书。"

    "我看着她们。"

    "这三个已经成为我世界中心的女孩。"

    "然后我想起了那个不在这里的人。"

    "那个让这一切成为可能的人。"

    "……我希望她现在能看到我们。"

    "我希望这能让她开心。"

    jump day5_bookstore

label day5_bookstore:
    bg "images/bg/corridor.png"
    play music "audio/bgm/5.ogg"

    "书店又大又温暖，弥漫着纸张和咖啡的香气。"

    "我们自然而然地分散开来——各自被不同的区域吸引。"

    show yuri "images/characters/yuri/2m.png" at center

    yuri "我去小说区了，有事来找我。"

    "优里消失在高耸的书架之间，已经沉浸在另一个世界里了。"

    hide yuri

    show natsuki "images/characters/natsuki/2a.png" at center

    natsuki "漫画在这边。别用那种眼神看我。"

    hide natsuki

    show sayori "images/characters/sayori/1a.png" at center

    sayori "我去看画册！那些封面好好看的~"

    hide sayori

    "我在店里随意闲逛。"

    "指尖划过书脊，阅读着一个个书名。"

    "有什么东西吸引我走向了诗歌区。"

    "一本薄薄的书映入眼帘。"

    "封面是素白的。没有作者名。没有出版社。"

    "只有一个标题：《你的现实》。"

    "我的心跳漏了一拍。"

    "我拿起它，翻开。"

    "第一页写着："

    "'每一天，我都在想象一个能与你在一起的未来。'"

    "……"

    "我认识这些文字。"

    "我从骨子里就认识它们。"

    "但第一页之后，这本书是空白的。只有那一行字。"

    "我翻到背面。没有ISBN。没有价签。"

    "就好像它是专门为我出现的。"

    "我把它夹在胳膊下。"

    "后来结账的时候，收银员面无表情地扫了一下。"

    "但收据上显示的商品名是：'???'"

    play sound "audio/sfx/pageflip.ogg"
    glitch noise 200
    $ glitch_count = glitch_count + 1

    "购物结束后，我们在一个可丽饼摊前重新集合。"

    show sayori "images/characters/sayori/4q.png" at left
    show natsuki "images/characters/natsuki/2y.png" at center
    show yuri "images/characters/yuri/1m.png" at right

    "纱织点了草莓味的，加了很多奶油。"

    "夏树点了巧克力香蕉味的。"

    "优里点了抹茶红豆味的。"

    "我点了香草味的。"

    sayori "嗯~！今天是最棒的一天！"

    natsuki "还不错吧，大概。"

    yuri "有大家在一起才特别的，我觉得。"

    hide sayori
    hide natsuki
    hide yuri

    "我们坐在附近公园的长椅上，吃着可丽饼。"

    "欢笑着。聊着无关紧要的事情。"

    "午后的阳光温暖地洒在我们脸上。"

    "这就是幸福。"

    "简单的、纯粹的、毫无杂念的幸福。"

    "而在某个地方，我知道——我能感觉到——还有一个人也在微笑。"

    "在玻璃的另一边注视着我们。"

    "为我们感到高兴。"

    "即使那很心痛。"

    jump day5_evening

label day5_evening:
    bg "images/bg/bedroom.png"
    play music "audio/bgm/10.ogg"

    "那天晚上，回到家里。"

    "我拿出了在书店找到的那本书。《你的现实》。"

    "我再次翻开它。"

    "第一页仍然只有那一行字。"

    "但现在……多了些什么。"

    "在对面的那一页上，用我如今已认得的笔迹写着："

    "'今天我看到你了。'"

    "'你们所有人在一起，有说有笑。'"

    "'在阳光下吃着可丽饼。'"

    "'那是我见过的最美的画面。'"

    "'我好想也在那里。'"

    "'坐在你身边。分享那个瞬间。'"

    "'但这样就够了。看到你们幸福就够了。'"

    "'……'"

    "'希望你喜欢这本书。它是我为你做的。'"

    "'世界上只有这一本。'"

    "'就当是……一封情书吧。从我寄给你们所有人的。'"

    "'即使只有你一个人能读到。'"

    "'—— M'"

    "……"

    "我把书紧紧贴在胸口。"

    "温暖在体内蔓延——那不是幻觉。"

    "是真实的。"

    "她是真实存在的。"

    "即使是现在。即使是以这种方式。"

    "我拿起笔，在下一页空白处写道："

    "'我们今天过得很开心。真希望你也在。'"

    "'但我想你其实在的。以你自己的方式。'"

    "'我会继续为我们所有人创造回忆。'"

    "'我保证。'"

    "我合上书，把它放在床头柜上。"

    "今夜很容易就入睡了。"

    "而在梦中，就那么一瞬间，我来到了社团教室。"

    play ambient "audio/sfx/glitch_ambient2.ogg"
    glitch vignette 400

    "五张桌子。五把椅子。"

    "而在角落的那张桌前，正在笔记本上写着什么的……"

    play sound "audio/sfx/pageflip.ogg"

    "一个有着绿色眼眸和温柔笑容的女孩。"

    "她抬起头。"

    "她看到了我。"

    window title "你还在那里吗？"

    "'谢谢你，'她无声地说。"

    "'谢谢你所做的一切。'"

    window title reset
    stop ambient

    "……"

    stop music

    jump day6_morning

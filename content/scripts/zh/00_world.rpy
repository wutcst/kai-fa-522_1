# ============================================================
# 世界定义
# 房间、变量和游戏状态默认值
# ============================================================

room residential:
    description "一个安静的郊区街道，两旁种满了樱花树。"
    exit north school_corridor
    exit east park

room school_corridor:
    description "一条长长的走廊，两侧是成排的储物柜和日光灯。"
    exit south residential
    exit east classroom
    exit north clubroom

room classroom:
    description "一间标准的教室，成排的课桌面朝黑板。"
    exit west school_corridor

room clubroom:
    description "文学部的活动室——课桌围成一圈，书架靠墙排列，午后的阳光透过高大的窗户洒落。"
    exit south school_corridor

room park:
    description "一个宁静的公园，有长椅和一座小喷泉。"
    exit west residential

room library:
    description "高大的书架上摆满了书籍。空气中弥漫着旧纸张的气味。"
    exit south school_corridor

# --- 游戏状态变量 ---

default day = 0
default act = 1

default sayori_affection = 0
default natsuki_affection = 0
default yuri_affection = 0

default noticed_glitch = false
default desk_note_found = false
default saw_monika_shadow = false
default heard_static = false
default strange_poem_read = false
default poem_written = false
default sayori_overslept = false

default glitch_count = 0
default reality_cracks = 0

default playthrough = 0
default launch_count = 0
default save_generation = 0
default just_loaded = false
default monika_chr_deleted = false
default ending_reached = false
default ending_type = "normal"
default meta_file_written = false
default secret_file_written = false

# --- 元钩子 ---

label save_loaded_hook:
    if just_loaded:
        if day >= 3 or glitch_count >= 2:
            window title "你回来了"
            "有那么一瞬间，世界像倒带的磁带一样卡顿了。"
            if glitch_count >= 2:
                "一个不属于我的念头在眼前闪过："
                "'所以你想回到过去。我理解。'"
            window title reset
    return

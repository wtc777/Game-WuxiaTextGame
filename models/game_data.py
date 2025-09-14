class GameData:
    def __init__(self):
        self.weapons = {
            "wooden_sword": {"name": "木剑", "attack": 5, "description": "练功用的木剑，轻巧但威力有限"},
            "iron_sword": {"name": "铁剑", "attack": 15, "description": "锋利的铁剑，江湖新手的好伙伴"},
            "steel_sword": {"name": "钢剑", "attack": 25, "description": "精钢锻造，削铁如泥"},
            "dragon_sword": {"name": "屠龙刀", "attack": 50, "description": "传说中的神兵，威力无穷"},
            "celestial_sword": {"name": "天剑", "attack": 80, "description": "仙人遗留的神器，蕴含天地之力"},
        }

        self.enemies = {
            "bandit": {"name": "山贼", "hp": 30, "attack": 8, "exp": 10, "gold": 5},
            "wolf": {"name": "恶狼", "hp": 25, "attack": 12, "exp": 15, "gold": 3},
            "assassin": {"name": "刺客", "hp": 40, "attack": 18, "exp": 25, "gold": 15},
            "boss_tiger": {"name": "虎王", "hp": 100, "attack": 30, "exp": 100, "gold": 50},
            "demon": {"name": "邪魔", "hp": 150, "attack": 45, "exp": 200, "gold": 100},
        }

        self.locations = {
            "village": {"name": "新手村", "description": "宁静的小村庄，这里是你冒险的起点"},
            "forest": {"name": "幽暗森林", "description": "危险的森林，野兽出没"},
            "mountain": {"name": "青云山", "description": "高耸入云的山峰，隐藏着无数秘密"},
            "city": {"name": "洛阳城", "description": "繁华的大城市，各路英雄汇聚之地"},
            "temple": {"name": "古刹", "description": "千年古寺，高僧云集之所"},
            "desert": {"name": "大漠", "description": "茫茫沙海，危机四伏"},
        }

        # 出身设定
        self.backgrounds = {
            "noble": {
                "name": "名门之后",
                "description": "出身武林世家，从小接受良好教育",
                "stats": {"hp": 20, "attack": 5, "gold": 100, "exp": 50},
                "story": "你出生于武林名门，家族世代行侠仗义。从小便接受严格的武学训练，虽然起点较高，但也背负着家族的荣誉与责任。"
            },
            "commoner": {
                "name": "平民百姓",
                "description": "普通人家出身，凭借努力习武",
                "stats": {"hp": 10, "attack": 3, "gold": 50, "exp": 0},
                "story": "你出生于普通农家，生活虽然清贫，但父母的关爱让你拥有坚强的意志。为了改变命运，你踏上了习武之路。"
            },
            "orphan": {
                "name": "孤儿",
                "description": "自幼失去双亲，在江湖中艰难生存",
                "stats": {"hp": 5, "attack": 8, "gold": 20, "exp": 30},
                "story": "你自幼失去双亲，在江湖的风风雨雨中长大。艰苦的生活磨练了你的意志，让你比同龄人更加坚韧和机警。"
            },
            "merchant": {
                "name": "商贾之家",
                "description": "家境富裕，但缺乏武学基础",
                "stats": {"hp": 15, "attack": 2, "gold": 200, "exp": 20},
                "story": "你出生于富商之家，从小衣食无忧。虽然家境富裕，但你渴望的不是金钱，而是江湖中的自由与冒险。"
            },
            "scholar": {
                "name": "书香门第",
                "description": "饱读诗书，智慧过人",
                "stats": {"hp": 8, "attack": 4, "gold": 80, "exp": 100},
                "story": "你出生于书香世家，从小饱读诗书，对武学理论了解颇深。虽然实战经验不足，但理论基础扎实。"
            }
        }

from flask import session
import random


class Player:
    def __init__(self, name, martial_art, background="commoner"):
        self.name = name
        self.martial_art = martial_art
        self.background = background
        self.level = 1
        self.age = 18  # 初始年龄
        self.hp = 100
        self.max_hp = 100
        self.attack = 10
        self.exp = 0
        self.exp_to_next = 50  # 升级所需经验
        self.gold = 50
        self.weapon = "wooden_sword"
        self.location = "village"
        self.story_progress = 0
        self.game_time = {"year": 1, "month": 1, "day": 1}  # 游戏内时间
        self.days_passed = 0

        # 根据出身调整初始属性
        # 注意：这里需要从game_data.backgrounds获取数据，但在重构后应该通过参数传入
        # 暂时保留原有逻辑，后续需要调整

    def to_dict(self):
        return {
            'name': self.name,
            'martial_art': self.martial_art,
            'background': self.background,
            'level': self.level,
            'age': self.age,
            'hp': self.hp,
            'max_hp': self.max_hp,
            'attack': self.attack,
            'exp': self.exp,
            'exp_to_next': self.exp_to_next,
            'gold': self.gold,
            'weapon': self.weapon,
            'location': self.location,
            'story_progress': self.story_progress,
            'game_time': self.game_time,
            'days_passed': self.days_passed
        }

    def level_up(self):
        if self.exp >= self.exp_to_next:
            self.exp -= self.exp_to_next
            self.level += 1
            self.max_hp += 20
            self.hp = self.max_hp
            self.attack += 5
            self.exp_to_next = self.level * 60  # 每级所需经验递增
            return True
        return False

    def age_up(self):
        """年龄增长，影响属性"""
        old_age = self.age
        self.age += 1

        # 年龄对属性的影响
        if self.age <= 25:
            # 青年期：属性稍有提升
            self.max_hp += random.randint(1, 3)
            self.attack += random.randint(0, 1)
        elif self.age <= 40:
            # 壮年期：属性提升较好
            self.max_hp += random.randint(2, 5)
            self.attack += random.randint(1, 2)
        elif self.age <= 60:
            # 中年期：属性增长缓慢
            self.max_hp += random.randint(0, 2)
            self.attack += random.randint(0, 1)
        else:
            # 老年期：体力下降但经验丰富
            self.max_hp -= random.randint(1, 3) if self.max_hp > 50 else 0
            self.attack += random.randint(0, 2)  # 经验弥补体力不足

        self.hp = self.max_hp  # 年龄增长时恢复满血

        return {"old_age": old_age, "new_age": self.age}

    def pass_time(self, days=1):
        """时间流逝"""
        self.days_passed += days

        # 更新游戏时间
        for _ in range(days):
            self.game_time["day"] += 1
            if self.game_time["day"] > 30:
                self.game_time["day"] = 1
                self.game_time["month"] += 1
                if self.game_time["month"] > 12:
                    self.game_time["month"] = 1
                    self.game_time["year"] += 1
                    # 每年年龄+1
                    return self.age_up()
        return None


def get_player():
    if 'player_data' in session:
        data = session['player_data']
        player = Player(data['name'], data['martial_art'], data.get('background', 'commoner'))
        player.level = data['level']
        player.age = data.get('age', 18)
        player.hp = data['hp']
        player.max_hp = data['max_hp']
        player.attack = data['attack']
        player.exp = data['exp']
        player.exp_to_next = data.get('exp_to_next', 50)
        player.gold = data['gold']
        player.weapon = data['weapon']
        player.location = data['location']
        player.story_progress = data['story_progress']
        player.game_time = data.get('game_time', {"year": 1, "month": 1, "day": 1})
        player.days_passed = data.get('days_passed', 0)
        return player
    return None


def save_player(player):
    session['player_data'] = player.to_dict()

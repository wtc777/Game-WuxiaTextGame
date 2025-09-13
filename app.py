from flask import Flask, request, jsonify, session
import random
import json
import os
import datetime

app = Flask(__name__, template_folder='.')
app.secret_key = 'wuxia_game_secret_key_2024'


# 游戏数据类
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


game_data = GameData()


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
        if background in game_data.backgrounds:
            bg_stats = game_data.backgrounds[background]["stats"]
            self.max_hp += bg_stats.get("hp", 0)
            self.hp = self.max_hp
            self.attack += bg_stats.get("attack", 0)
            self.gold += bg_stats.get("gold", 0)
            self.exp += bg_stats.get("exp", 0)

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


def get_time_string(player):
    """获取时间字符串"""
    time = player.game_time
    return f"武林历{time['year']}年{time['month']}月{time['day']}日"


@app.route('/')
def index():
    with open('templates/index.html', 'r', encoding='utf-8') as f:
        return f.read()


@app.route('/get_backgrounds')
def get_backgrounds():
    return jsonify({'backgrounds': game_data.backgrounds})


@app.route('/create_character', methods=['POST'])
def create_character():
    data = request.json
    name = data.get('name')
    martial_art = data.get('martial_art')
    background = data.get('background', 'commoner')

    if not name or not martial_art:
        return jsonify({'error': '请填写完整信息'})

    player = Player(name, martial_art, background)
    save_player(player)

    bg_info = game_data.backgrounds.get(background, {})
    time_str = get_time_string(player)

    return jsonify({
        'success': True,
        'message': f'[{time_str}] 欢迎你，{name}！你选择了{martial_art}作为你的武学流派，出身{bg_info.get("name", "未知")}。{bg_info.get("story", "")}',
        'player': player.to_dict()
    })


@app.route('/game_status')
def game_status():
    player = get_player()
    if not player:
        return jsonify({'error': '请先创建角色'})

    weapon_info = game_data.weapons.get(player.weapon, {})
    location_info = game_data.locations.get(player.location, {})
    background_info = game_data.backgrounds.get(player.background, {})

    return jsonify({
        'player': player.to_dict(),
        'weapon_info': weapon_info,
        'location_info': location_info,
        'background_info': background_info,
        'time_string': get_time_string(player)
    })


@app.route('/explore', methods=['POST'])
def explore():
    player = get_player()
    if not player:
        return jsonify({'error': '请先创建角色'})

    if player.hp <= 0:
        return jsonify({'error': '你已经死亡，请休息恢复'})

    # 时间流逝
    age_result = player.pass_time(random.randint(1, 3))
    time_str = get_time_string(player)

    # 随机事件
    event_type = random.choice(['enemy', 'treasure', 'story', 'nothing'])

    messages = []

    if age_result:
        messages.append(
            f"[{time_str}] 岁月如流水，你已经{age_result['new_age']}岁了。随着年龄的增长，你的实力也在发生变化...")

    if event_type == 'enemy':
        enemy_key = random.choice(list(game_data.enemies.keys()))
        enemy = game_data.enemies[enemy_key].copy()
        session['current_enemy'] = {'key': enemy_key, 'data': enemy}

        messages.append(f"[{time_str}] 你遇到了{enemy['name']}！")

        return jsonify({
            'type': 'enemy',
            'messages': messages,
            'enemy': enemy
        })

    elif event_type == 'treasure':
        gold_found = random.randint(5, 20)
        player.gold += gold_found
        save_player(player)

        messages.append(f"[{time_str}] 你发现了一个宝箱，获得了{gold_found}金币！")

        return jsonify({
            'type': 'treasure',
            'messages': messages,
            'gold_gained': gold_found
        })

    elif event_type == 'story':
        stories = [
            "你遇到了一位神秘的老者，他传授给你一些武学心得。",
            "你发现了一座古老的石碑，上面刻着前人的武功感悟。",
            "一只受伤的小鸟落在你面前，你温柔地为它包扎了伤口，内心感到平静。",
            "你路过一处风景秀丽的地方，观察山川流水，对武学有了新的理解。",
            "你遇到了一位同道中人，与他切磋武艺，互有收获。",
            "在一处客栈中，你听到了江湖传说，心中对武道的追求更加坚定。"
        ]

        # 随机获得少量经验
        exp_gained = random.randint(5, 15)
        player.exp += exp_gained

        # 检查升级
        level_up_msg = ""
        if player.level_up():
            level_up_msg = f" 恭喜！你升级到了{player.level}级！"

        save_player(player)

        messages.append(f"[{time_str}] {random.choice(stories)}你获得了{exp_gained}点经验。{level_up_msg}")

        return jsonify({
            'type': 'story',
            'messages': messages,
            'exp_gained': exp_gained
        })

    else:
        messages.append(f"[{time_str}] 你在周围探索了一番，但什么都没有发现。时间悄悄流逝...")
        save_player(player)

        return jsonify({
            'type': 'nothing',
            'messages': messages
        })


@app.route('/battle', methods=['POST'])
def battle():
    player = get_player()
    if not player:
        return jsonify({'error': '请先创建角色'})

    if 'current_enemy' not in session:
        return jsonify({'error': '没有正在战斗的敌人'})

    enemy = session['current_enemy']['data']
    action = request.json.get('action')
    time_str = get_time_string(player)

    if action == 'attack':
        # 玩家攻击
        weapon_info = game_data.weapons.get(player.weapon, {})
        player_damage = player.attack + weapon_info.get('attack', 0) + random.randint(-3, 3)
        enemy['hp'] -= player_damage

        battle_log = [f'[{time_str}] 你对{enemy["name"]}造成了{player_damage}点伤害！']

        if enemy['hp'] <= 0:
            # 敌人死亡
            exp_gained = session['current_enemy']['data']['exp']
            gold_gained = session['current_enemy']['data']['gold']

            player.exp += exp_gained
            player.gold += gold_gained

            battle_log.append(f'[{time_str}] {enemy["name"]}被击败了！')
            battle_log.append(f'[{time_str}] 获得{exp_gained}经验值和{gold_gained}金币！')

            # 检查升级
            if player.level_up():
                battle_log.append(f'[{time_str}] 恭喜！你升级到了{player.level}级！')

            # 战斗胜利后时间流逝
            age_result = player.pass_time(1)
            if age_result:
                battle_log.append(f'经过激烈的战斗，你已经{age_result["new_age"]}岁了。')

            save_player(player)
            del session['current_enemy']

            return jsonify({
                'victory': True,
                'battle_log': battle_log,
                'exp_gained': exp_gained,
                'gold_gained': gold_gained
            })

        else:
            # 敌人反击
            enemy_damage = enemy['attack'] + random.randint(-2, 2)
            player.hp -= enemy_damage
            battle_log.append(f'[{time_str}] {enemy["name"]}对你造成了{enemy_damage}点伤害！')

            if player.hp <= 0:
                player.hp = 0
                battle_log.append(f'[{time_str}] 你被击败了！')
                save_player(player)

                return jsonify({
                    'defeat': True,
                    'battle_log': battle_log
                })

            save_player(player)
            session['current_enemy']['data'] = enemy

            return jsonify({
                'continue': True,
                'battle_log': battle_log,
                'enemy_hp': enemy['hp']
            })

    elif action == 'flee':
        if random.random() < 0.7:  # 70%逃跑成功率
            del session['current_enemy']
            return jsonify({
                'fled': True,
                'message': f'[{time_str}] 你成功逃跑了！'
            })
        else:
            enemy_damage = enemy['attack'] + random.randint(-2, 2)
            player.hp -= enemy_damage
            save_player(player)

            return jsonify({
                'flee_failed': True,
                'message': f'[{time_str}] 逃跑失败！{enemy["name"]}对你造成了{enemy_damage}点伤害！',
                'enemy_hp': enemy['hp']
            })


@app.route('/rest', methods=['POST'])
def rest():
    player = get_player()
    if not player:
        return jsonify({'error': '请先创建角色'})

    cost = 10
    if player.gold < cost:
        return jsonify({'error': '金币不足，休息需要10金币'})

    player.gold -= cost
    player.hp = player.max_hp

    # 休息时间流逝
    age_result = player.pass_time(random.randint(1, 2))
    time_str = get_time_string(player)

    save_player(player)

    message = f'[{time_str}] 你在客栈好好休息了一番，体力完全恢复了！'
    if age_result:
        message += f' 在休息中，你已经{age_result["new_age"]}岁了。'

    return jsonify({
        'success': True,
        'message': message,
        'hp_restored': player.max_hp
    })


@app.route('/shop')
def shop():
    return jsonify({
        'weapons': game_data.weapons
    })


@app.route('/buy_weapon', methods=['POST'])
def buy_weapon():
    player = get_player()
    if not player:
        return jsonify({'error': '请先创建角色'})

    weapon_key = request.json.get('weapon')
    weapon = game_data.weapons.get(weapon_key)

    if not weapon:
        return jsonify({'error': '武器不存在'})

    # 简单的价格计算
    price = weapon['attack'] * 10

    if player.gold < price:
        return jsonify({'error': f'金币不足！需要{price}金币'})

    player.gold -= price
    player.weapon = weapon_key

    time_str = get_time_string(player)
    save_player(player)

    return jsonify({
        'success': True,
        'message': f'[{time_str}] 成功购买了{weapon["name"]}！',
        'weapon': weapon
    })


@app.route('/save_game', methods=['POST'])
def save_game():
    player = get_player()
    if not player:
        return jsonify({'error': '没有角色数据可保存'})

    save_data = {
        'player': player.to_dict(),
        'timestamp': datetime.datetime.now().isoformat(),
        'version': '1.0'
    }

    # 保存到session中（在实际项目中可以保存到数据库或文件）
    session['saved_game'] = save_data

    return jsonify({
        'success': True,
        'message': '游戏保存成功！',
        'save_time': save_data['timestamp']
    })


@app.route('/load_game', methods=['POST'])
def load_game():
    if 'saved_game' not in session:
        return jsonify({'error': '没有找到存档'})

    save_data = session['saved_game']
    session['player_data'] = save_data['player']

    return jsonify({
        'success': True,
        'message': f'游戏读取成功！存档时间：{save_data["timestamp"]}',
        'player': save_data['player']
    })


@app.route('/get_save_info')
def get_save_info():
    if 'saved_game' not in session:
        return jsonify({'has_save': False})

    save_data = session['saved_game']
    player_data = save_data['player']

    return jsonify({
        'has_save': True,
        'save_info': {
            'name': player_data['name'],
            'level': player_data['level'],
            'age': player_data['age'],
            'timestamp': save_data['timestamp']
        }
    })


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
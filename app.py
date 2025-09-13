from flask import Flask, render_template, request, jsonify, session
import random
import json
import os

app = Flask(__name__)
app.secret_key = 'wuxia_game_secret_key_2024'

# 游戏数据类
class GameData:
    def __init__(self):
        self.weapons = {
            "wooden_sword": {"name": "木剑", "attack": 5, "description": "练功用的木剑，轻巧但威力有限"},
            "iron_sword": {"name": "铁剑", "attack": 15, "description": "锋利的铁剑，江湖新手的好伙伴"},
            "steel_sword": {"name": "钢剑", "attack": 25, "description": "精钢锻造，削铁如泥"},
            "dragon_sword": {"name": "屠龙刀", "attack": 50, "description": "传说中的神兵，威力无穷"},
        }
        
        self.enemies = {
            "bandit": {"name": "山贼", "hp": 30, "attack": 8, "exp": 10, "gold": 5},
            "wolf": {"name": "恶狼", "hp": 25, "attack": 12, "exp": 15, "gold": 3},
            "assassin": {"name": "刺客", "hp": 40, "attack": 18, "exp": 25, "gold": 15},
            "boss_tiger": {"name": "虎王", "hp": 100, "attack": 30, "exp": 100, "gold": 50},
        }
        
        self.locations = {
            "village": {"name": "新手村", "description": "宁静的小村庄，这里是你冒险的起点"},
            "forest": {"name": "幽暗森林", "description": "危险的森林，野兽出没"},
            "mountain": {"name": "青云山", "description": "高耸入云的山峰，隐藏着无数秘密"},
            "city": {"name": "洛阳城", "description": "繁华的大城市，各路英雄汇聚之地"},
        }

game_data = GameData()

class Player:
    def __init__(self, name, martial_art):
        self.name = name
        self.martial_art = martial_art
        self.level = 1
        self.hp = 100
        self.max_hp = 100
        self.attack = 10
        self.exp = 0
        self.gold = 50
        self.weapon = "wooden_sword"
        self.location = "village"
        self.story_progress = 0

    def to_dict(self):
        return {
            'name': self.name,
            'martial_art': self.martial_art,
            'level': self.level,
            'hp': self.hp,
            'max_hp': self.max_hp,
            'attack': self.attack,
            'exp': self.exp,
            'gold': self.gold,
            'weapon': self.weapon,
            'location': self.location,
            'story_progress': self.story_progress
        }

    def level_up(self):
        if self.exp >= self.level * 50:
            self.exp -= self.level * 50
            self.level += 1
            self.max_hp += 20
            self.hp = self.max_hp
            self.attack += 5
            return True
        return False

def get_player():
    if 'player_data' in session:
        data = session['player_data']
        player = Player(data['name'], data['martial_art'])
        player.level = data['level']
        player.hp = data['hp']
        player.max_hp = data['max_hp']
        player.attack = data['attack']
        player.exp = data['exp']
        player.gold = data['gold']
        player.weapon = data['weapon']
        player.location = data['location']
        player.story_progress = data['story_progress']
        return player
    return None

def save_player(player):
    session['player_data'] = player.to_dict()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/create_character', methods=['POST'])
def create_character():
    data = request.json
    name = data.get('name')
    martial_art = data.get('martial_art')
    
    if not name or not martial_art:
        return jsonify({'error': '请填写完整信息'})
    
    player = Player(name, martial_art)
    save_player(player)
    
    return jsonify({
        'success': True,
        'message': f'欢迎你，{name}！你选择了{martial_art}作为你的武学流派。',
        'player': player.to_dict()
    })

@app.route('/game_status')
def game_status():
    player = get_player()
    if not player:
        return jsonify({'error': '请先创建角色'})
    
    weapon_info = game_data.weapons.get(player.weapon, {})
    location_info = game_data.locations.get(player.location, {})
    
    return jsonify({
        'player': player.to_dict(),
        'weapon_info': weapon_info,
        'location_info': location_info
    })

@app.route('/explore', methods=['POST'])
def explore():
    player = get_player()
    if not player:
        return jsonify({'error': '请先创建角色'})
    
    if player.hp <= 0:
        return jsonify({'error': '你已经死亡，请休息恢复'})
    
    # 随机事件
    event_type = random.choice(['enemy', 'treasure', 'story', 'nothing'])
    
    if event_type == 'enemy':
        enemy_key = random.choice(list(game_data.enemies.keys()))
        enemy = game_data.enemies[enemy_key].copy()
        session['current_enemy'] = {'key': enemy_key, 'data': enemy}
        
        return jsonify({
            'type': 'enemy',
            'message': f'你遇到了{enemy["name"]}！',
            'enemy': enemy
        })
    
    elif event_type == 'treasure':
        gold_found = random.randint(5, 20)
        player.gold += gold_found
        save_player(player)
        
        return jsonify({
            'type': 'treasure',
            'message': f'你发现了一个宝箱，获得了{gold_found}金币！',
            'gold_gained': gold_found
        })
    
    elif event_type == 'story':
        stories = [
            "你遇到了一位神秘的老者，他给了你一些人生的启示。",
            "你发现了一座古老的石碑，上面刻着神秘的武功心法。",
            "一只受伤的小鸟落在你面前，你温柔地为它包扎了伤口。",
            "你路过一处风景秀丽的地方，心情变得愉悦起来。"
        ]
        
        return jsonify({
            'type': 'story',
            'message': random.choice(stories)
        })
    
    else:
        return jsonify({
            'type': 'nothing',
            'message': '你在周围探索了一番，但什么都没有发现。'
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
    
    if action == 'attack':
        # 玩家攻击
        weapon_info = game_data.weapons.get(player.weapon, {})
        player_damage = player.attack + weapon_info.get('attack', 0) + random.randint(-3, 3)
        enemy['hp'] -= player_damage
        
        battle_log = [f'你对{enemy["name"]}造成了{player_damage}点伤害！']
        
        if enemy['hp'] <= 0:
            # 敌人死亡
            exp_gained = session['current_enemy']['data']['exp']
            gold_gained = session['current_enemy']['data']['gold']
            
            player.exp += exp_gained
            player.gold += gold_gained
            
            battle_log.append(f'{enemy["name"]}被击败了！')
            battle_log.append(f'获得{exp_gained}经验值和{gold_gained}金币！')
            
            # 检查升级
            if player.level_up():
                battle_log.append(f'恭喜！你升级到了{player.level}级！')
            
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
            battle_log.append(f'{enemy["name"]}对你造成了{enemy_damage}点伤害！')
            
            if player.hp <= 0:
                player.hp = 0
                battle_log.append('你被击败了！')
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
                'message': '你成功逃跑了！'
            })
        else:
            enemy_damage = enemy['attack'] + random.randint(-2, 2)
            player.hp -= enemy_damage
            save_player(player)
            
            return jsonify({
                'flee_failed': True,
                'message': f'逃跑失败！{enemy["name"]}对你造成了{enemy_damage}点伤害！',
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
    save_player(player)
    
    return jsonify({
        'success': True,
        'message': '你在客栈好好休息了一番，体力完全恢复了！',
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
    save_player(player)
    
    return jsonify({
        'success': True,
        'message': f'成功购买了{weapon["name"]}！',
        'weapon': weapon
    })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
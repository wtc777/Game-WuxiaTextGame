from flask import Blueprint, request, jsonify, session
from models.player import get_player, save_player
from services.exploration_service import ExplorationService
from services.battle_service import BattleService
from models.game_data import GameData

# 创建蓝图
game_api = Blueprint('game_api', __name__)

# 初始化服务
game_data = GameData()
exploration_service = ExplorationService(game_data)
battle_service = BattleService(game_data)


@game_api.route('/explore', methods=['POST'])
def explore():
    player = get_player()
    if not player:
        return jsonify({'error': '请先创建角色'})

    try:
        result = exploration_service.explore(player)
        save_player(player)
        return jsonify(result)
    except ValueError as e:
        return jsonify({'error': str(e)})


@game_api.route('/battle', methods=['POST'])
def battle():
    player = get_player()
    if not player:
        return jsonify({'error': '请先创建角色'})

    data = request.json
    action = data.get('action')

    try:
        result = battle_service.process_attack(player, action)
        save_player(player)
        return jsonify(result)
    except ValueError as e:
        return jsonify({'error': str(e)})


@game_api.route('/rest', methods=['POST'])
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
    time_str = exploration_service.get_time_string(player)

    save_player(player)

    message = f'[{time_str}] 你在客栈好好休息了一番，体力完全恢复了！'
    if age_result:
        message += f' 在休息中，你已经{age_result["new_age"]}岁了。'

    return jsonify({
        'success': True,
        'message': message,
        'hp_restored': player.max_hp
    })


# 数据库相关API
@game_api.route('/save_game', methods=['POST'])
def save_game():
    player = get_player()
    if not player:
        return jsonify({'error': '没有角色数据可保存'})

    try:
        # 使用数据库保存游戏
        from utils.database import DatabaseManager
        db_manager = DatabaseManager()
        db_manager.save_game(player)
        
        return jsonify({
            'success': True,
            'message': '游戏保存成功！'
        })
    except Exception as e:
        return jsonify({'error': f'保存失败: {str(e)}'})


@game_api.route('/load_game', methods=['POST'])
def load_game():
    from utils.database import DatabaseManager
    db_manager = DatabaseManager()
    
    # 从session获取玩家名称
    if 'player_data' in session:
        player_name = session['player_data']['name']
        save_data = db_manager.load_game(player_name)
        
        if save_data:
            session['player_data'] = save_data['player']
            return jsonify({
                'success': True,
                'message': f'游戏读取成功！存档时间：{save_data["timestamp"]}',
                'player': save_data['player']
            })
    
    return jsonify({'error': '没有找到存档'})


@game_api.route('/get_save_info')
def get_save_info():
    from utils.database import DatabaseManager
    db_manager = DatabaseManager()
    
    # 从session获取玩家名称
    if 'player_data' in session:
        player_name = session['player_data']['name']
        save_info = db_manager.get_save_info(player_name)
        
        if save_info:
            return jsonify({
                'has_save': True,
                'save_info': save_info
            })
    
    return jsonify({'has_save': False})

from flask import Blueprint, request, jsonify, session
from models.player import get_player, save_player
from services.shop_service import ShopService
from models.game_data import GameData

# 创建蓝图
shop_api = Blueprint('shop_api', __name__)

# 初始化服务
game_data = GameData()
shop_service = ShopService(game_data)


@shop_api.route('/shop')
def shop():
    weapons = shop_service.get_shop_items()
    return jsonify({'weapons': weapons})


@shop_api.route('/buy_weapon', methods=['POST'])
def buy_weapon():
    player = get_player()
    if not player:
        return jsonify({'error': '请先创建角色'})

    data = request.json
    weapon_key = data.get('weapon')

    try:
        result = shop_service.buy_weapon(player, weapon_key)
        time_str = get_time_string(player)
        save_player(player)
        
        return jsonify({
            'success': True,
            'message': f'[{time_str}] 成功购买了{result["weapon"]["name"]}！',
            'weapon': result["weapon"]
        })
    except ValueError as e:
        return jsonify({'error': str(e)})


def get_time_string(player):
    """获取时间字符串"""
    time = player.game_time
    return f"武林历{time['year']}年{time['month']}月{time['day']}日"

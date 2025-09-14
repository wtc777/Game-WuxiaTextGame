from flask import Blueprint, request, jsonify, session
from models.player import save_player
from services.character_service import CharacterService
from models.game_data import GameData

# 创建蓝图
character_api = Blueprint('character_api', __name__)

# 初始化服务
game_data = GameData()
character_service = CharacterService(game_data)


@character_api.route('/get_backgrounds')
def get_backgrounds():
    return jsonify({'backgrounds': game_data.backgrounds})


@character_api.route('/create_character', methods=['POST'])
def create_character():
    data = request.json
    name = data.get('name')
    martial_art = data.get('martial_art')
    background = data.get('background', 'commoner')

    try:
        player = character_service.create_character(name, martial_art, background)
        save_player(player)

        bg_info = game_data.backgrounds.get(background, {})
        time_str = character_service.get_time_string(player)

        return jsonify({
            'success': True,
            'message': f'[{time_str}] 欢迎你，{name}！你选择了{martial_art}作为你的武学流派，出身{bg_info.get("name", "未知")}。{bg_info.get("story", "")}',
            'player': player.to_dict()
        })
    except ValueError as e:
        return jsonify({'error': str(e)})


@character_api.route('/game_status')
def game_status():
    from models.player import get_player
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
        'time_string': character_service.get_time_string(player)
    })

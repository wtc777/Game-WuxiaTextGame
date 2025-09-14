from models.player import Player
from models.game_data import GameData
import random


class CharacterService:
    def __init__(self, game_data: GameData):
        self.game_data = game_data

    def create_character(self, name, martial_art, background="commoner"):
        """创建新角色"""
        if not name or not martial_art:
            raise ValueError("请填写完整信息")

        player = Player(name, martial_art, background)
        
        # 根据出身调整初始属性
        if background in self.game_data.backgrounds:
            bg_stats = self.game_data.backgrounds[background]["stats"]
            player.max_hp += bg_stats.get("hp", 0)
            player.hp = player.max_hp
            player.attack += bg_stats.get("attack", 0)
            player.gold += bg_stats.get("gold", 0)
            player.exp += bg_stats.get("exp", 0)
            
        return player

    def get_time_string(self, player):
        """获取时间字符串"""
        time = player.game_time
        return f"武林历{time['year']}年{time['month']}月{time['day']}日"

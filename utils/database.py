import sqlite3
import json
import os
from datetime import datetime
from models.player import Player


class DatabaseManager:
    def __init__(self, db_path="game_data.db"):
        self.db_path = db_path
        self.init_database()

    def init_database(self):
        """初始化数据库表"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # 创建玩家表
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS players (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                data TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # 创建存档表
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS saves (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                player_id INTEGER,
                save_name TEXT,
                data TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (player_id) REFERENCES players (id)
            )
        ''')
        
        conn.commit()
        conn.close()

    def save_player(self, player: Player):
        """保存玩家数据到数据库"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        player_data = json.dumps(player.to_dict())
        
        # 检查玩家是否已存在
        cursor.execute("SELECT id FROM players WHERE name = ?", (player.name,))
        result = cursor.fetchone()
        
        if result:
            # 更新现有玩家
            cursor.execute(
                "UPDATE players SET data = ?, updated_at = ? WHERE name = ?",
                (player_data, datetime.now(), player.name)
            )
        else:
            # 创建新玩家
            cursor.execute(
                "INSERT INTO players (name, data) VALUES (?, ?)",
                (player.name, player_data)
            )
        
        conn.commit()
        conn.close()

    def load_player(self, player_name):
        """从数据库加载玩家数据"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("SELECT data FROM players WHERE name = ?", (player_name,))
        result = cursor.fetchone()
        conn.close()
        
        if result:
            player_data = json.loads(result[0])
            return self.dict_to_player(player_data)
        return None

    def dict_to_player(self, player_data):
        """将字典转换为Player对象"""
        player = Player(
            player_data['name'],
            player_data['martial_art'],
            player_data.get('background', 'commoner')
        )
        player.level = player_data['level']
        player.age = player_data.get('age', 18)
        player.hp = player_data['hp']
        player.max_hp = player_data['max_hp']
        player.attack = player_data['attack']
        player.exp = player_data['exp']
        player.exp_to_next = player_data.get('exp_to_next', 50)
        player.gold = player_data['gold']
        player.weapon = player_data['weapon']
        player.location = player_data['location']
        player.story_progress = player_data['story_progress']
        player.game_time = player_data.get('game_time', {"year": 1, "month": 1, "day": 1})
        player.days_passed = player_data.get('days_passed', 0)
        return player

    def save_game(self, player: Player, save_name="auto_save"):
        """保存游戏进度"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # 获取玩家ID
        cursor.execute("SELECT id FROM players WHERE name = ?", (player.name,))
        result = cursor.fetchone()
        
        if not result:
            # 如果玩家不存在，先保存玩家
            self.save_player(player)
            cursor.execute("SELECT id FROM players WHERE name = ?", (player.name,))
            result = cursor.fetchone()
        
        player_id = result[0]
        save_data = json.dumps({
            'player': player.to_dict(),
            'timestamp': datetime.now().isoformat(),
            'version': '1.0'
        })
        
        # 检查是否已有同名存档
        cursor.execute(
            "SELECT id FROM saves WHERE player_id = ? AND save_name = ?",
            (player_id, save_name)
        )
        result = cursor.fetchone()
        
        if result:
            # 更新现有存档
            cursor.execute(
                "UPDATE saves SET data = ?, created_at = ? WHERE player_id = ? AND save_name = ?",
                (save_data, datetime.now(), player_id, save_name)
            )
        else:
            # 创建新存档
            cursor.execute(
                "INSERT INTO saves (player_id, save_name, data) VALUES (?, ?, ?)",
                (player_id, save_name, save_data)
            )
        
        conn.commit()
        conn.close()

    def load_game(self, player_name, save_name="auto_save"):
        """加载游戏进度"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # 获取玩家ID
        cursor.execute("SELECT id FROM players WHERE name = ?", (player_name,))
        result = cursor.fetchone()
        
        if not result:
            conn.close()
            return None
            
        player_id = result[0]
        
        # 获取存档数据
        cursor.execute(
            "SELECT data FROM saves WHERE player_id = ? AND save_name = ?",
            (player_id, save_name)
        )
        result = cursor.fetchone()
        conn.close()
        
        if result:
            save_data = json.loads(result[0])
            return save_data
        return None

    def get_save_info(self, player_name):
        """获取存档信息"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # 获取玩家ID
        cursor.execute("SELECT id FROM players WHERE name = ?", (player_name,))
        result = cursor.fetchone()
        
        if not result:
            conn.close()
            return None
            
        player_id = result[0]
        
        # 获取所有存档信息
        cursor.execute(
            "SELECT save_name, created_at FROM saves WHERE player_id = ?",
            (player_id,)
        )
        results = cursor.fetchall()
        conn.close()
        
        return [{"save_name": row[0], "created_at": row[1]} for row in results]

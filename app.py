from flask import Flask, render_template
from config import config
from models.game_data import GameData
from api.character_api import character_api
from api.game_api import game_api
from api.shop_api import shop_api

# 初始化游戏数据
game_data = GameData()

def create_app(config_name='default'):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    
    # 注册蓝图
    app.register_blueprint(character_api)
    app.register_blueprint(game_api)
    app.register_blueprint(shop_api)
    
    @app.route('/')
    def index():
        return render_template('index.html')
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, host='0.0.0.0', port=5000)

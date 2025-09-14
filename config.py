import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'wuxia_game_secret_key_2024'
    DATABASE_PATH = os.environ.get('DATABASE_PATH') or 'game_data.db'
    
class DevelopmentConfig(Config):
    DEBUG = True

class ProductionConfig(Config):
    DEBUG = False

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}

import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """기본 설정"""
    DEBUG = False
    TESTING = False
    JSON_AS_ASCII = False
    JSON_SORT_KEYS = False

class DevelopmentConfig(Config):
    """개발 환경 설정"""
    DEBUG = True
    MYSQL_HOST = os.getenv('MYSQL_HOST', 'localhost')
    MYSQL_USER = os.getenv('MYSQL_USER', 'root')
    MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD', '')
    MYSQL_DB = os.getenv('MYSQL_DB', 'bone_report')
    MYSQL_PORT = int(os.getenv('MYSQL_PORT', 3306))

class ProductionConfig(Config):
    """프로덕션 환경 설정"""
    DEBUG = False
    MYSQL_HOST = os.getenv('MYSQL_HOST')
    MYSQL_USER = os.getenv('MYSQL_USER')
    MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD')
    MYSQL_DB = os.getenv('MYSQL_DB')
    MYSQL_PORT = int(os.getenv('MYSQL_PORT', 3306))

def get_config():
    """환경에 따른 설정 반환"""
    env = os.getenv('FLASK_ENV', 'development')
    if env == 'production':
        return ProductionConfig
    return DevelopmentConfig

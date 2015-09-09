"""

Configurations
--------------

Various setups for different app instances

"""


class Config:
    """Default config"""

    DEBUG = False
    TESTING = False
    SECRET_KEY = 'flask+braiiin=<3'
    SESSION_STORE = 'session'
    LIVE = []
    STATIC_PATH = 'static'
    HASHING_ROUNDS = 15

    INIT = {
        'port': 8005,
        'host': '127.0.0.1',
    }


class ProductionConfig(Config):
    """Production vars"""
    LOGIC_URI = 'http://logic.outline.braiiin.com'
    CORE_URI = 'http://braiiin.com'


class DevelopmentConfig(Config):
    """For local runs"""
    DEBUG = True
    LOGIC_URI = 'http://localhost:8006'
    CORE_URI = 'http://localhost:8000'


class TestConfig(Config):
    """For automated testing"""
    LOGIC_URI = 'http://localhost:8006'
    TESTING = True

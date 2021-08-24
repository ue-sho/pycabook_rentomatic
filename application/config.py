import os

# abspath : パス名 path の正規化された絶対パスを返す
# pathの正規化とは、./ や ../ を除去して表すこと
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    """Base configuration"""


class ProductionConfig(Config):
    """Production configuration"""


class DevelopmentConfig(Config):
    """Development configuration"""


class TestingConfig(Config):
    """Testing configuration"""

    TESTING = True
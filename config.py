class Config:
    SECRET_KEY = "SunshineSucks"

    @staticmethod
    def init_app(app):
        pass

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'mysql://Jesse:cheeseit007@localhost/talebase'

config = {
    'development': DevelopmentConfig
}
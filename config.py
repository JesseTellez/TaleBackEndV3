class Config:
    SECRET_KEY = "SunshineSucks"

    @staticmethod
    def init_app(app):
        pass

class DevelopmentConfig(Config):
    DEBUG = True
    #This is either root or Jesse depending on what comp im on
    SQLALCHEMY_DATABASE_URI = 'mysql://root:cheeseit007@localhost/talebase'

config = {
    'SECRET_KEY': "SunshineSucks",
    'development': DevelopmentConfig
}
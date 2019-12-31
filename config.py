class Configuration:
    DEBUG = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://valsl:etereg14@localhost/test1'
    # 7) Добавление Secret Key
    SECRET_KEY = 'secret'

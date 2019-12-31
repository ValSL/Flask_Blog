class Configuration:
    DEBUG = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://valsl:etereg14@localhost/test1'
    # 7) Добавление Secret Key (Далее создание моделей)
    SECRET_KEY = 'secret'

    # 15) Соль и хэш(Дальше шаблоны, переопределение login_user.html )
    SECURITY_PASSWORD_SALT = 'salt'
    SECURITY_PASSWORD_HASH = 'sha512_crypt'
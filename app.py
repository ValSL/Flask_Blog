from flask import Flask
from config import Configuration
from flask_sqlalchemy import SQLAlchemy

from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager

# 1) Импорт класса админ
from flask_admin import Admin
# 3) Импорт класса ModelView для наших моделей БД
from flask_admin.contrib.sqla import ModelView


app = Flask(__name__, template_folder='templates')
app.config.from_object(Configuration)

db = SQLAlchemy(app)

migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)  # (название команды, команда)


# 5) Наши модели
from models import *

# Admin #
# 2) Создание экземпляра класса Admin
admin = Admin(app)

# 4) Добвавление в админку нашу таблицу Post
admin.add_view(ModelView(Post, db.session))

# 6) Добвавление в админку нашу таблицу Tag (потом в конфиг)
admin.add_view(ModelView(Tag, db.session))
from flask import Flask
from config import Configuration
from flask_sqlalchemy import SQLAlchemy

from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from flask import redirect, url_for, request

# 1) Импорт класса админ
from flask_admin import Admin
# 3) Импорт класса ModelView для наших моделей БД
from flask_admin.contrib.sqla import ModelView

# 10) Подключение SQLAlchemyUserDatastore, для хранения юзеров
from flask_security import SQLAlchemyUserDatastore

# 13) Подключение самого класса Security(далее в блюпринт),  юзеры пока без ролей
from flask_security import Security

# 17)
from flask_security import current_user

app = Flask(__name__, template_folder='templates')
app.config.from_object(Configuration)

db = SQLAlchemy(app)

migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)  # (название команды, команда)


# 5) Наши модели
from models import *

# 16) В новом классе AdminView переопределим методы из ModelView, чтобы ограничить доступ
class AdminView(ModelView):
    #Метод проверят доступность вьюхи пользователю
    def is_accessible(self):
        return current_user.has_role('admin')

    #Если какая-то конкретная вьюха не доступна, то выполнится этот метод
    def inaccessible_callback(self, name, **kwargs):
        # Тут обращаемся к блюпринту security  его вьюхе login, Параметр next это та ссылка куда пользователь хотел попасть
        return redirect(url_for('security.login', next=request.url))


# Admin #
# 2) Создание экземпляра класса Admin
admin = Admin(app)

# 4) Добвавление в админку нашу таблицу Post
admin.add_view(AdminView(Post, db.session))

# 6) Добвавление в админку нашу таблицу Tag (потом в конфиг)
admin.add_view(AdminView(Tag, db.session))


# Flask secutiry
# 11) экземпляр userDataStore
user_datastore = SQLAlchemyUserDatastore(db, User, Role)

# 12) Подключение FlaskSecurity, принимает наше приложение и хранилище
secutiry = Security(app, user_datastore)


### юзеры создаются через user_datastore.create_user(email='', password='') ###
### роли тоже user_datastore.create_role(name='', description='') ###
### роли добавляются через user_datastore.add_role_to_user(user, role) ###

### Каим образом мы даём права именно роли с именем 'admin'
### Мы в base.html будем показывать ссылку на админку только юзерам с этой ролью
### Поэтому идём в base.html
### Потом интегрируем security и admin в app.py

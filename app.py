from flask import Flask
from config import Configuration
from flask_sqlalchemy import SQLAlchemy

from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from flask import redirect, url_for, request

# 1) Импорт класса админ
from flask_admin import Admin

# 19)
from flask_admin import AdminIndexView

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

# 22) чтобы не был одинаковый код в AdminView и HomeAdminView
class AdminMixin:
    #### ПОЛУЧАЕТСЯ ЧТО МЕТОДЫ is_accessible И inaccessible_callback ЕСТЬ И В ModelView и в AdminIndexView которые мы импортировали
    # Метод проверят доступность вьюхи пользователю
    def is_accessible(self):
        return current_user.has_role('admin')

    # Если какая-то конкретная вьюха не доступна, то выполнится этот метод
    def inaccessible_callback(self, name, **kwargs):
        # Тут обращаемся к блюпринту security  его вьюхе login, Параметр next это та ссылка куда пользователь хотел попасть
        return redirect(url_for('security.login', next=request.url))


# 21) flask admin создает объекты наших постов по своему, поэтому создание постов через саму админку приводит к пустому слагу и мы это исправляем
class BaseModelView(ModelView):
    # Переопределяем метод, который говорит, если модель изменяется или создается вызвать generate_slug()
    def on_model_change(self, form, model, is_created):
        model.generate_slug()
        return super().on_model_change(form, model, is_created)



# 16) В новом классе AdminView переопределим методы из ModelView, чтобы ограничить доступ для просмотра Post и Tag во вкладке /admin
class AdminView(AdminMixin, ModelView):
    pass


# 18) Ограничение доступа целиком к админке
# как я понял если мы вводим в сторку в браузере /admin выполняется эта функция, требует логина, если мы не админ, и вазвращает True если мы админ, и потом переходит в админку на окно home кторое указали мы ниже
class HomeAdminView(AdminMixin, AdminIndexView):
    pass


# 23) т.к. generate_slug импользуют только Post и Tag и изменяем в 92 и 89 строке AdminView на соответствующие
class PostAdminView(AdminMixin, BaseModelView):
    # изменим вид создания или изменения постов в админке
    form_columns = ['title', 'body', 'tags']

class TagAdminView(AdminMixin, BaseModelView):
    form_columns = ['name', 'posts']




# Admin #
# 2) Создание экземпляра класса Admin
# 20) 'Главная FlaskApp кнопочка на админке ведет на url='/', тоесть на сайт,index_view=HomeAdminView(name='Home') там будет кнопочка home которя включает HomeAdminView'
admin = Admin(app, 'FlaskApp', url='/', index_view=HomeAdminView(name='Home'))

# 4) Добвавление в админку нашу таблицу Post
admin.add_view(PostAdminView(Post, db.session))

# 6) Добвавление в админку нашу таблицу Tag (потом в конфиг)
admin.add_view(TagAdminView(Tag, db.session))


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

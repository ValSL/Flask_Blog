from flask import Blueprint
from flask import render_template

from models import Post, Tag

from flask import request

from .forms import PostForm

from app import db

from flask import redirect
from flask import url_for

# posts - название блюпринта
posts = Blueprint('posts', __name__, template_folder='templates')


@posts.route('/create', methods=['POST', 'GET'])
def create_post():
    if request.method == 'POST':
        title = request.form['title']  # 'title' это переменная title из класса PostForm
        body = request.form['body']

        try:
            post = Post(title=title, body=body)
            db.session.add(post)
            db.session.commit()
        except:
            print('Wrong')
        return redirect(url_for('posts.index'))

    form = PostForm()
    return render_template('posts/create_post.html', form=form)


@posts.route('/')
def index():
    # 'q' то что мы ввели в base.html Search
    q = request.args.get('q')

    if q:
        posts = Post.query.filter(Post.title.contains(q) | Post.body.contains(q)).all()
    else:
        posts = Post.query.order_by(Post.created.desc())

    return render_template('posts/index.html', posts=posts)


@posts.route('/<slug>')
def post_detail(slug):
    post = Post.query.filter(Post.slug == slug).first()
    tags = post.tags
    return render_template('posts/post_detail.html', post=post, tags=tags)


@posts.route('/tag/<slug>')
def tag_detail(slug):
    tag = Tag.query.filter(Tag.slug == slug).first()
    '''all нужет чтобы получть тип списка, без all будет типо BaseQuery.
     Метод all  доступен потому что в ralationship'е 
     мы указали lazy=dynamic что возвращает тип BaseQuery
     и у BaseQuery есть много разных методов'''
    posts = tag.posts.all()
    return render_template('posts/tag_detail.html', tag=tag, posts=posts)

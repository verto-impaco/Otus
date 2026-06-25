import os
import time

from flask import Flask, flash, redirect, render_template, request, url_for
from sqlalchemy import create_engine, select
from sqlalchemy.exc import IntegrityError, OperationalError
from sqlalchemy.orm import scoped_session, sessionmaker

from models import Base, Post, User


app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "secret")


def get_db_url():
    db_url = os.environ.get("SQLALCHEMY_DATABASE_URI")
    if db_url:
        return db_url

    old_url = os.environ.get("SQLALCHEMY_PG_CONN_URI")
    if old_url:
        return old_url.replace("postgresql+asyncpg://", "postgresql+psycopg://")

    return "postgresql+psycopg://postgres:password@localhost/postgres"


engine = create_engine(get_db_url(), pool_pre_ping=True)
Session = scoped_session(sessionmaker(bind=engine, expire_on_commit=False))
db_ready = False


def create_tables():
    for _ in range(10):
        try:
            Base.metadata.create_all(engine)
            return
        except OperationalError:
            time.sleep(2)

    Base.metadata.create_all(engine)


@app.before_request
def before_request():
    global db_ready
    if not db_ready:
        create_tables()
        db_ready = True


@app.teardown_appcontext
def shutdown_session(exception=None):
    Session.remove()


@app.get("/")
def index():
    return redirect(url_for("posts"))


@app.get("/users")
def users():
    session = Session()
    users_list = session.scalars(select(User).order_by(User.id)).all()
    return render_template("users.html", users=users_list)


@app.route("/users/new", methods=["GET", "POST"])
def new_user():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        username = request.form.get("username", "").strip()
        email = request.form.get("email", "").strip()

        if not name or not username or not email:
            flash("Заполните все поля.")
        else:
            session = Session()
            session.add(User(name=name, username=username, email=email))
            try:
                session.commit()
            except IntegrityError:
                session.rollback()
                flash("Такой username или email уже есть.")
            else:
                return redirect(url_for("users"))

    return render_template("user_form.html", form=request.form)


@app.get("/posts")
def posts():
    session = Session()
    posts_list = session.scalars(select(Post).order_by(Post.id.desc())).all()
    return render_template("posts.html", posts=posts_list)


@app.route("/posts/new", methods=["GET", "POST"])
def new_post():
    session = Session()

    if request.method == "POST":
        user_id = request.form.get("user_id", "")
        title = request.form.get("title", "").strip()
        body = request.form.get("body", "").strip()

        try:
            user = session.get(User, int(user_id))
        except ValueError:
            user = None

        if not user:
            flash("Сначала выберите автора.")
        elif not title or not body:
            flash("Заполните заголовок и текст.")
        else:
            session.add(Post(userId=user.id, title=title, body=body))
            session.commit()
            return redirect(url_for("posts"))

    users_list = session.scalars(select(User).order_by(User.id)).all()
    return render_template("post_form.html", users=users_list, form=request.form)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=False)

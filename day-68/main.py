import os

from flask import Flask, render_template, request, url_for, redirect, flash, send_from_directory, session
import flask
from flask_wtf import FlaskForm
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String
import sqlalchemy as sa
from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, Email

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret-key-goes-here'

# set up flask_login's LoginManager
app.secret_key = '1d179a0cf2b2c1ad1dd577138326de0eab75615ea3447ecd0c0e8033a646f067'
login_manager = LoginManager()
login_manager.init_app(app)

# CREATE DATABASEs


class Base(DeclarativeBase):
    pass

script_dir = os.path.dirname(os.path.abspath(__file__))
file_dir = os.path.join(script_dir,'instance','users.db')
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{file_dir}'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
db = SQLAlchemy(model_class=Base)
db.init_app(app)

# CREATE TABLE IN DB


class User(db.Model, UserMixin):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    email: Mapped[str] = mapped_column(String(100), unique=True)
    password: Mapped[str] = mapped_column(String(100))
    name: Mapped[str] = mapped_column(String(1000))

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

# SETUP LoginManager
login_manager = LoginManager()
login_manager.init_app(app)

# CREATE FORMS

class RegisterForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    email = StringField('Email Address', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])

class LoginForm(FlaskForm):
    email = StringField('Email Address', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    

with app.app_context():
    db.create_all()


@app.route('/')
def home():
    return render_template("index.html", logged_in=current_user.is_authenticated)


@app.route('/register', methods=["GET", "POST"])
def register():
    form = RegisterForm()

    if form.validate_on_submit():

        user = db.session.scalar(
            sa.select(User).where(User.email == form.email.data)
        )

        if user:
            flash("You've already signed up with that email, login instead!")
            return redirect(url_for('login'))

        hash_and_salted_password = generate_password_hash(
            password=form.password.data,
            method='pbkdf2:sha256',
            salt_length=8
        )

        user = User(
            email = form.email.data,
            password = hash_and_salted_password,
            name = form.name.data
        )

        db.session.add(user)
        db.session.commit()

        return redirect(url_for('secrets', name=form.name.data))
    else:
        print("form not valid")
        print(form.errors)

    return render_template("register.html", form=form)


@app.route('/login', methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    form = LoginForm()

    if form.validate_on_submit():
        user = db.session.scalar(
            sa.select(User).where(User.email == form.email.data)
        )

        if user is None:
            flash("Invalid email address, please try again.")
            return redirect(url_for('login'))
        
        if not user.check_password(form.password.data):
            flash("Invalid password, please try again.")
            return redirect(url_for('login'))

        login_user(user)
        return redirect(url_for('secrets', name=user.name))

    return render_template("login.html", form=form)


@app.route('/secrets?name=<name>')
@login_required
def secrets(name):
    return render_template("secrets.html", name=name, logged_in=current_user.is_authenticated)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route('/download')
def download():
    return send_from_directory("static", path="files/cheat_sheet.pdf")


@login_manager.user_loader
def load_user(user_id):
    return db.get_or_404(User, user_id)

# from https://github.com/django/django/blob/4.0/django/utils/http.py#L239
def url_has_allowed_host_and_scheme(url, allowed_hosts, require_https=False):
    """
    Return ``True`` if the url uses an allowed host and a safe scheme.

    Always return ``False`` on an empty url.

    If ``require_https`` is ``True``, only 'https' will be considered a valid
    scheme, as opposed to 'http' and 'https' with the default, ``False``.

    Note: "True" doesn't entail that a URL is "safe". It may still be e.g.
    quoted incorrectly. Ensure to also use django.utils.encoding.iri_to_uri()
    on the path component of untrusted URLs.
    """
    if url is not None:
        url = url.strip()
    if not url:
        return False
    if allowed_hosts is None:
        allowed_hosts = set()
    elif isinstance(allowed_hosts, str):
        allowed_hosts = {allowed_hosts}
    # Chrome treats \ completely as / in paths but it could be part of some
    # basic auth credentials so we need to check both URLs.
    return (
        _url_has_allowed_host_and_scheme(url, allowed_hosts, require_https=require_https) and
        _url_has_allowed_host_and_scheme(url.replace('\\', '/'), allowed_hosts, require_https=require_https)
    )

if __name__ == "__main__":
    app.run(debug=True)

import os

from flask import Flask, render_template, request, url_for, redirect, flash, send_from_directory
from flask_wtf import FlaskForm
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String
from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, Email

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret-key-goes-here'

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


class User(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    email: Mapped[str] = mapped_column(String(100), unique=True)
    password: Mapped[str] = mapped_column(String(100))
    name: Mapped[str] = mapped_column(String(1000))

class RegisterForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    email = StringField('Email Address', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])


with app.app_context():
    db.create_all()


@app.route('/')
def home():
    return render_template("index.html")


@app.route('/register', methods=["GET", "POST"])
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        print(form.data)

        user = User(
            email = form.email.data,
            password = form.password.data,
            name = form.name.data
        )

        db.session.add(user)
        db.session.commit()

        return redirect(url_for('secrets', name=form.name.data))
    else:
        print("form not valid")
        print(form.errors)

    return render_template("register.html", form=form)


@app.route('/login')
def login():
    return render_template("login.html")


@app.route('/secrets?name=<name>')
def secrets(name):
    return render_template("secrets.html", name=name)


@app.route('/logout')
def logout():
    pass


@app.route('/download')
def download():
    return send_from_directory("static", path="files/cheat_sheet.pdf")
    pass


if __name__ == "__main__":
    app.run(debug=True)

import os

from flask import Flask, jsonify, render_template, redirect, url_for
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Text
from flask_wtf import FlaskForm
from wtforms import IntegerField, StringField, SubmitField, HiddenField
from wtforms.validators import DataRequired, URL
from wtforms.widgets import HiddenInput
from flask_ckeditor import CKEditor, CKEditorField
from flask_ckeditor.utils import cleanify
import datetime

'''
Make sure the required packages are installed: 
Open the Terminal in PyCharm (bottom left). 

On Windows type:
python -m pip install -r requirements.txt

On MacOS type:
pip3 install -r requirements.txt

This will install the packages from the requirements.txt for this project.
'''

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
app.config['CKEDITOR_PKG_TYPE'] = 'standard'
ckeditor = CKEditor(app)
Bootstrap5(app)

# CREATE DATABASE
class Base(DeclarativeBase):
    pass
script_dir = os.path.dirname(os.path.abspath(__file__))
file_dir = os.path.join(script_dir,'instance','posts.db')
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///posts.db'
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{file_dir}'
db = SQLAlchemy(model_class=Base)
db.init_app(app)


# CONFIGURE TABLE
class BlogPost(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    subtitle: Mapped[str] = mapped_column(String(250), nullable=False)
    date: Mapped[str] = mapped_column(String(250), nullable=False)
    body: Mapped[str] = mapped_column(Text, nullable=False)
    author: Mapped[str] = mapped_column(String(250), nullable=False)
    img_url: Mapped[str] = mapped_column(String(250), nullable=False)


with app.app_context():
    db.create_all()

class PostForm(FlaskForm):
    # id = IntegerField('id', widget=HiddenInput())
    title = StringField('Blog Post Title', validators=[DataRequired()])
    subtitle = StringField('Subtitle', validators=[DataRequired()])
    author = StringField('Your Name', validators=[DataRequired()])
    img_url = StringField('Blog Image URL', validators=[DataRequired()])
    body = CKEditorField('Blog Content', validators=[DataRequired()])
    submit = SubmitField('Submit Post', validators=[DataRequired()])

"""
create a PostForm object, populating the fiedls if the blog_post parameter
has a value
"""
# def CreatePostForm(blog_post: BlogPost | None):
#     form = PostForm()

#     if blog_post:
#         form.id.data = blog_post.id
#         form.author.data = blog_post.author
#         form.body.data = blog_post.body
#         form.img_url.data = blog_post.img_url
#         form.subtitle.data = blog_post.subtitle
#         form.title.data = blog_post.title

#     return form
def CreatePostForm(title, subtitle, img_url, author, body):
    form = PostForm()
    form.title.data = title
    form.subtitle.data = subtitle
    form.img_url.data = img_url
    form.author.data = author
    form.body.data = body

    return form

@app.route('/')
def get_all_posts():
    posts = db.session.execute(db.select(BlogPost)).scalars().all()
    return render_template("index.html", all_posts=posts)


@app.route('/post?post_id=<int:post_id>')
def show_post(post_id):
    requested_post = db.session.get(entity=BlogPost, ident=post_id)
    return render_template("post.html", post=requested_post)


# TODO: add_new_post() to create a new blog post
@app.route("/new-post", methods=["GET", "POST"])
def create_post():
    form = PostForm()
    # form = CreatePostForm(None)

    valid_form = form.validate_on_submit()
    if not valid_form:
        print(f"form errors:\n{form.errors}")

    if valid_form:
        x = datetime.datetime.now() 

        post = BlogPost(
            title = form.title.data,
            subtitle = form.subtitle.data,
            date = x.strftime("%B %d, %Y"),
            body = form.body.data,
            author = form.author.data,
            img_url = form.img_url.data
        )

        print(f"post data:\n {post.__dict__}")

        db.session.add(post)
        db.session.commit()
        return redirect(url_for('get_all_posts'))

    return render_template("make-post.html", form=form, is_edit=False)


# TODO: edit_post() to change an existing blog post
# @app.route("/edit-post/<int:post_id>", methods=["GET", "POST"])
# def edit_post(post_id):
#     # form = PostForm()
#     # blog_post = db.session.get(entity=BlogPost, ident=post_id)

#     # if blog_post:
#     #     if form.validate_on_submit():
#     #         print("form is valid!")
#     #         if form.id.data:
#     #             blog_post.id = form.id.data
#     #         blog_post.title = form.title.data
#     #         blog_post.subtitle = form.subtitle.data
#     #         blog_post.img_url = form.img_url.data
#     #         blog_post.body = form.body.data

#     #         print(f"blog post to update:\n{blog_post.__dict__}")

#     #         db.session.commit()

#     #         return redirect(url_for('show_post', post_id=blog_post.id))
#     #     else:
#     #         print("form is not valid!")
#     #         form = CreatePostForm(blog_post)
#     #         return render_template("make-post.html", form=form, is_edit=True)
#     # else:
#     #     return jsonify(error = {
#     #         "message": "no blog post were found matching the blog_id"
#     #     })
#     post = db.get_or_404(BlogPost, post_id)
#     edit_form = CreatePostForm(
#         title = post.title,
#         subtitle=post.subtitle,
#         img_url=post.img_url,
#         author=post.author,
#         body = post.body
#     )

#     if edit_form.validate_on_submit():
#         post.title = edit_form.title.data
#         post.subtitle = edit_form.subtitle.data
#         post.img_url = edit_form.img_url.data
#         post.author = edit_form.author.data
#         post.body = edit_form.body.data

#         print(f"blog post to update:\n{post.__dict__}")

#         db.session.commit()

#         return redirect(url_for('show_post', post_id=post.id))
    
#     return render_template("make-post.html", form=edit_form, is_edit=True)
@app.route("/edit-post/<int:post_id>", methods=["GET", "POST"])
def edit_post(post_id):
    edit_form = PostForm()
    
    post = db.session.get(BlogPost, post_id)

    if edit_form.validate_on_submit():
        print("form is valid!")
        post.title = edit_form.title.data
        post.subtitle = edit_form.subtitle.data
        post.img_url = edit_form.img_url.data
        post.author = edit_form.author.data
        post.body = edit_form.body.data    

        print(f"post data:\n{post.__dict__}")
        
        # db.session.merge(post)
        db.session.commit()
        return redirect(url_for("show_post", post_id=post.id))

    edit_form = CreatePostForm(
        title=post.title,
        subtitle=post.subtitle,
        img_url=post.img_url,
        author=post.author,
        body=post.body
    )
    
    return render_template("make-post.html", form=edit_form, is_edit=True)


# TODO: delete_post() to remove a blog post from the database

# Below is the code from previous lessons. No changes needed.
@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/contact")
def contact():
    return render_template("contact.html")


if __name__ == "__main__":
    app.run(debug=True, port=5003)

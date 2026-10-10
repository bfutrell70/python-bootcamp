import requests
from flask import Flask, render_template


app = Flask(__name__)
blog_url = 'https://api.npoint.io/c790b4d5cab58020d391'
blog_response = requests.get(blog_url)
all_posts = blog_response.json()


@app.route('/')
def home():

    return render_template("index.html", posts=all_posts)

@app.route('/post/<int:blog_id>')
def show_post(blog_id):
    print(blog_id)
    post = [ b for b in all_posts if b['id'] == blog_id ][0]
    print(post)
    return render_template("post.html", post=post)

if __name__ == "__main__":
    app.run(debug=True)

from flask import Flask, render_template
from post import Posts

app = Flask(__name__)

posts = Posts()

@app.route('/')
def home():
    return render_template("index.html")

@app.route("/blog")
def blog():
    all_posts = posts.get_all_posts()
    return render_template("blog.html", posts=all_posts)

@app.route("/post/<int:index>")
def post(index):
    requested_post = posts.get_post(index)
    return render_template("post.html", post=requested_post)

if __name__ == "__main__":
    app.run(debug=True)

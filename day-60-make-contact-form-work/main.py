from flask import Flask, render_template
from post import Posts

app = Flask(__name__)
posts = Posts()

@app.route("/")
def home():
    return render_template("index.html", posts=posts.all_posts)

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/contact")
def contact():
    return render_template("contact.html")

@app.route("/post/<int:id>")
def post(id):
    return render_template("post.html", post=posts.get_post(id))

@app.route("/form-entry", methods=["POST"])
def receive_data():
    return "<h1>Successfully sent your message</h1>"

if __name__ == "__main__":
    app.run(debug=True)
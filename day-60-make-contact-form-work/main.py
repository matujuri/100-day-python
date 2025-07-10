from flask import Flask, render_template, request
from post import Posts
from notification_manager import NotificationManager

app = Flask(__name__)
posts = Posts()
notification_manager = NotificationManager()

@app.route("/")
def home():
    return render_template("index.html", posts=posts.all_posts)

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        notification_manager.send_email(
            to_addrs=request.form['email'],
            subject="New Message from Blog Contact Form",
            message=f"Name: {request.form['name']}\nEmail: {request.form['email']}\nPhone: {request.form['phone']}\nMessage: {request.form['message']}"
        )
    return render_template("contact.html")

@app.route("/post/<int:id>")
def post(id):
    return render_template("post.html", post=posts.get_post(id))

if __name__ == "__main__":
    app.run(debug=True)
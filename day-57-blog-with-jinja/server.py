from flask import Flask, render_template
import random
from datetime import datetime
import requests

def get_gender(name):
    response = requests.get(f"https://api.genderize.io?name={name}")
    print(response.json())
    response.raise_for_status()
    return response.json()["gender"]

def get_age(name):
    response = requests.get(f"https://api.agify.io?name={name}")
    print(response.json())
    response.raise_for_status()
    return response.json()["age"]

app = Flask(__name__)

@app.route('/')
def home():
    random_number = random.randint(0, 9)
    year = datetime.now().year
    return render_template("index.html", num=random_number, year=year)

@app.route("/guess/<name>")
def guess(name):
    gender = get_gender(name)
    age = get_age(name)
    return render_template("guess.html", name=name, gender=gender, age=age)

@app.route("/blog")
def blog():
    response = requests.get("https://api.npoint.io/c790b4d5cab58020d391")
    response.raise_for_status()
    all_posts = response.json()
    return render_template("blog.html", posts=all_posts)

if __name__ == "__main__":
    app.run(debug=True)
    
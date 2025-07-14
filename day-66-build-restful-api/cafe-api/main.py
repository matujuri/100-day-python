from flask import Flask, jsonify, render_template, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Boolean
import os
import random
'''
Install the required packages first: 
Open the Terminal in PyCharm (bottom left). 

On Windows type:
python -m pip install -r requirements.txt

On MacOS type:
pip3 install -r requirements.txt

This will install the packages from requirements.txt for this project.
'''

app = Flask(__name__)

# CREATE DB
class Base(DeclarativeBase):
    pass
# Connect to Database
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(os.path.dirname(__file__), 'cafes.db')}"
db = SQLAlchemy(model_class=Base)
db.init_app(app)


# Cafe TABLE Configuration
class Cafe(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    map_url: Mapped[str] = mapped_column(String(500), nullable=False)
    img_url: Mapped[str] = mapped_column(String(500), nullable=False)
    location: Mapped[str] = mapped_column(String(250), nullable=False)
    seats: Mapped[str] = mapped_column(String(250), nullable=False)
    has_toilet: Mapped[bool] = mapped_column(Boolean, nullable=False)
    has_wifi: Mapped[bool] = mapped_column(Boolean, nullable=False)
    has_sockets: Mapped[bool] = mapped_column(Boolean, nullable=False)
    can_take_calls: Mapped[bool] = mapped_column(Boolean, nullable=False)
    coffee_price: Mapped[str] = mapped_column(String(250), nullable=True)
    
    def to_dict(self):
        return {column.name: getattr(self, column.name) for column in self.__table__.columns} # type: ignore[attr-defined]

with app.app_context():
    db.create_all()


@app.route("/")
def home():
    return render_template("index.html")

# HTTP GET - Read Record

@app.route("/random")
def get_random_cafe():
    cafes = db.session.execute(db.select(Cafe)).scalars().all()
    random_cafe = random.choice(cafes).to_dict()
    return jsonify(cafe=random_cafe)

@app.route("/all")
def get_all_cafes():
    cafes = db.session.execute(db.select(Cafe)).scalars().all()
    return jsonify(cafes=[cafe.to_dict() for cafe in cafes])

@app.route("/search")
def search_cafe():
    location = request.args.get("loc")
    cafes = db.session.execute(db.select(Cafe).where(Cafe.location == location)).scalars().all()
    if cafes:
        return jsonify(cafes=[cafe.to_dict() for cafe in cafes])
    else:
        return jsonify(error={"Not Found": "Sorry, we don't have a cafe st that location."})

# HTTP POST - Create Record
@app.route("/add", methods=["POST"])
def add_cafe():
    if not request.form.get("name"):
        return jsonify(error={"Bad Request": "name is required."}), 400
    if not request.form.get("map_url"):
        return jsonify(error={"Bad Request": "map_url is required."}), 400
    if not request.form.get("img_url"):
        return jsonify(error={"Bad Request": "img_url is required."}), 400
    if not request.form.get("location"):
        return jsonify(error={"Bad Request": "location is required."}), 400
    if not request.form.get("seats"):
        return jsonify(error={"Bad Request": "seats is required."}), 400
    if not request.form.get("has_toilet"):
        return jsonify(error={"Bad Request": "has_toilet is required."}), 400
    if not request.form.get("has_wifi"):
        return jsonify(error={"Bad Request": "has_wifi is required."}), 400
    if not request.form.get("has_sockets"):
        return jsonify(error={"Bad Request": "has_sockets is required."}), 400
    if not request.form.get("can_take_calls"):
        return jsonify(error={"Bad Request": "can_take_calls is required."}), 400
   
    new_cafe = Cafe(
        name=request.form.get("name"),
        map_url=request.form.get("map_url"),
        img_url=request.form.get("img_url"),
        location=request.form.get("location"),
        seats=request.form.get("seats"),
        has_toilet=bool(request.form.get("has_toilet")),
        has_wifi=bool(request.form.get("has_wifi")),
        has_sockets=bool(request.form.get("has_sockets")),
        can_take_calls=bool(request.form.get("can_take_calls")),
        coffee_price=request.form.get("coffee_price"),
    )
    db.session.add(new_cafe)
    db.session.commit()
    return jsonify(response={"success": "Successfully added the new cafe."}), 200


# HTTP PUT/PATCH - Update Record

@app.route("/update-price/<int:cafe_id>", methods=["PATCH"])
def update_price(cafe_id):
    new_price = request.args.get("new_price")
    if not new_price:
        return jsonify(error={"error": "new_price is required."}), 400
    try:
        cafe = db.get_or_404(Cafe, cafe_id)
        cafe.coffee_price = new_price # type: ignore[report-attribute-type]
        db.session.commit()
        return jsonify(response={"success": "Successfully updated the price."}), 200
    except Exception as e:
        return jsonify(error={"Not Found": "Sorry a cafe with that id was not found in the database."}), 404

# HTTP DELETE - Delete Record

@app.route("/report-closed/<int:cafe_id>", methods=["DELETE"])
def report_closed(cafe_id):
    api_key = request.args.get("api_key")
    if not api_key or api_key != "TopSecretAPIKey":
        return jsonify(error={"error": "Sorry, that's not allowed. Make sure you have the correct api_key."}), 403
    try:
        cafe = db.get_or_404(Cafe, cafe_id)
        db.session.delete(cafe)
        db.session.commit()
        return jsonify(response={"success": "Successfully deleted the cafe."}), 200
    except Exception as e:
        return jsonify(error={"Not Found": "Sorry a cafe with that id was not found in the database."}), 404


if __name__ == '__main__':
    app.run(debug=True)
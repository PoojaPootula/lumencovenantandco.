from flask import Flask, render_template, request, redirect, url_for
from models import db, Card
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///lumen.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["UPLOAD_FOLDER"] = "static/uploads/cards"

db.init_app(app)

with app.app_context():
    db.create_all()

def save_image(image_file):
    if image_file and image_file.filename:

        filename = secure_filename(image_file.filename)

        filepath = os.path.join(
            app.config["UPLOAD_FOLDER"],
            filename
        )

        image_file.save(filepath)

        return filename

    return None

@app.route("/")
def home():
    return render_template("home.html")


@app.route("/admin/cards", methods=["GET", "POST"])
def admin_cards():

    if request.method == "POST":

        front_filename = save_image(request.files.get("front_image"))
        left_filename = save_image(request.files.get("inside_left_image"))
        right_filename = save_image(request.files.get("inside_right_image"))
        back_filename = save_image(request.files.get("back_image"))

        card = Card(
            name=request.form["name"],
            short_description=request.form["description"],

            front_image=front_filename,
            inside_left_image=left_filename,
            inside_right_image=right_filename,
            back_image=back_filename,

            featured="featured" in request.form,
            active="active" in request.form
        )

        db.session.add(card)
        db.session.commit()

        return redirect(url_for("admin_cards"))

    cards = Card.query.all()

    return render_template(
        "admin/cards.html",
        cards=cards
    )

@app.route("/admin/cards/<int:card_id>/edit",
           methods=["GET", "POST"])
def edit_card(card_id):

    card = Card.query.get_or_404(card_id)

    if request.method == "POST":

        card.name = request.form["name"]
        card.short_description = request.form["description"]

        card.featured = "featured" in request.form
        card.active = "active" in request.form

        db.session.commit()

        return redirect(url_for("admin_cards"))

    return render_template("admin/edit_card.html", card=card)

@app.route("/admin/cards/<int:card_id>/delete", methods=["POST"])
def delete_card(card_id):

    card = Card.query.get_or_404(card_id)

    db.session.delete(card)
    db.session.commit()

    return redirect(url_for("admin_cards"))

if __name__ == "__main__":
    app.run(debug=True)
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timezone

db = SQLAlchemy()

class Collection(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(50), nullable=False)
    cover_photo = db.Column(db.String(255))
class Card(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(50), nullable=False)
    slug = db.Column(db.String(120), unique=True)
    description = db.Column(db.Text)

    front_image = db.Column(db.String(255))
    inside_left_image = db.Column(db.String(255))
    inside_right_image = db.Column(db.String(255))
    back_image = db.Column(db.String(255))

    featured = db.Column(db.Boolean, default=False)

    active = db.Column(db.Boolean, default=True)

    created_at = db.Column(
        db.DateTime,
        default=datetime.now(timezone.utc)
    )
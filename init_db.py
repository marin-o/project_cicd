from app import app, db
from models import Artist, Album, Song

with app.app_context():
    db.create_all()

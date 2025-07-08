from ext import app, db
from models import Food, User,Rating, Booking

with app.app_context():
    db.drop_all()
    db.create_all()


    admin = User(username="admin", password="adminpass", role="Admin")
    admin.create()
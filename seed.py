from myrecipes import db
from models import User, Recipe, Collections

db.drop_all()
db.create_all()
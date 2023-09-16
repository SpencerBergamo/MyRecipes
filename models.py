from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy

bcrypt = Bcrypt()
db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name= db.Column(db.Text, nullable=False)
    last_name= db.Column(db.Text, nullable=False)
    email= db.Column(db.Text, nullable=False, unique=True)
    username= db.Column(db.Text, nullable=False, unique=True)
    password = db.Column(db.Text, nullable=False)


    collections = db.relationship(
        'Collections', 
        cascade="all, delete-orphan")

    # recipe = db.relationship(
    #     'Recipe',
    #     cascade="all, delete-orphan")

    @classmethod
    def signup(cls, first_name, last_name, email, username, password):
        hashed_pwd = bcrypt.generate_password_hash(password).decode('UTF-8')
        user = User(
            first_name=first_name,
            last_name=last_name,
            email=email,
            username=username,
            password=hashed_pwd,
            )
        db.session.add(user)
        return user
    
    @classmethod
    def authenticate(cls, username, password):
        user = User.query.filter_by(username=username).first()
        if user and bcrypt.check_password_hash(user.password, password):
            return user
        else: 
            return False   
        
class Collections(db.Model):
    __tablename__ = 'collections'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='cascade'), nullable=False)
    user = db.relationship('User', backref='collections')
    # recipes = db.relationship('Recipe', backref='recipebook', cascade="all, delete-orphan")

    @classmethod
    def add_collection(cls, title, user_id):
        collection = Collections(
            title=title,
            user_id=user_id
        )
        db.session.add(collection)
        db.session.commit()
        return collection
    
    user = db.relationship('User')

class Recipe(db.Model):
    __tablename__ = 'recipe'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    recipe_id = db.Column(db.Integer, nullable=False)
    title = db.Column(db.Text, nullable=False)
    image = db.Column(db.Text, nullable=True)
    collections_id = db.Column(db.Integer, db.ForeignKey('collections.id'), nullable=False)
    collections = db.relationship('Collections', backref='recipe')
    # collections_id = db.Column(db.Integer, db.ForeignKey('collections.id', ondelete='cascade'), nullable=False)
    # ingredients = db.Column(db.Text, nullable=True)
    # instructions = db.Column(db.Text, nullable=True)
    # image = db.Column(db.Text, nullable=True)
    # url = db.Column(db.Text, nullable=True)
    # name = db.Column(db.Text, nullable=True)
    # user = db.relationship('User', secondary='collections', backref='recipe')


# class TempRecipe(db.Model):
#     __tablename__ = 'temprecipe'

#     id = db.Column(db.Integer, primary_key=True)
#     recipe_id = db.Column(db.Integer, nullable=False)
#     title = db.Column(db.String(255), nullable=False)
#     image = db.Column(db.String(255))
#     ingredients = db.Column(db.JSON)
#     instructions = db.Column(db.JSON)
#     name = db.Column(db.String(255))
#     url = db.Column(db.String(255))


#     def __init__(self, title, image, ingredients, instructions, name, url):
#         self.title = title
#         self.image = image
#         self.ingredients = ingredients
#         self.instructions = instructions
#         self.name = name
#         self.url = url

def connect_db(app):
    
    db.app = app
    db.init_app(app)
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, SelectField, BooleanField
from wtforms.validators import InputRequired, Length, NumberRange, URL, Optional, Email

class UserLoginForm(FlaskForm):
    username = StringField("Username", validators=[InputRequired(message="Username required"), Length(max=20)])
    password = PasswordField("Password", validators=[InputRequired(message="Password required"), Length(max=55)])

class UserAddForm(FlaskForm):
    first_name = StringField("First Name", validators=[InputRequired(message="First name required"), Length(max=30)])
    last_name = StringField("Last Name", validators=[InputRequired(message="Last name required"), Length(max=30)])
    email = StringField("Email", validators=[InputRequired(message="Email required"), Length(max=50), Email(message="Invalid email")])
    username = StringField("Username", validators=[InputRequired(message="Username required"), Length(max=20)])
    password = PasswordField("Password", validators=[InputRequired(message="Password required"), Length(max=55)])

class AddDiet(FlaskForm):
    diet = SelectField("Diet", choices=[
        ("glute_free", "Gluten Free"), 
        ("ketogenic", "Ketogenic"), 
        ("vegetarian", "Vegetarian"), 
        ("lacto_vegetarian", "Lacto-Vegetarian"),
        ("ovo_vegetarian", "Ovo-Vegetarian"),
        ("vegan", "vegan"),
        ("pescetarian", "Pescetarian"),
        ("paleo", "Paleo"),
        ("primal", "Primal"),
        ("whole30", "Whole30"),
        ("none", "None")
        ])


class UserEditForm(FlaskForm):
    username = StringField("Username", validators=[InputRequired(message="Username required"), Length(max=20)])
    email = StringField("Email", validators=[InputRequired(message="Email required"), Length(max=50), Email(message="Invalid email")])
    first_name = StringField("First Name", validators=[InputRequired(message="First name required"), Length(max=30)])
    last_name = StringField("Last Name", validators=[InputRequired(message="Last name required"), Length(max=30)])

# I need to add forms for recipes and recipe books, but i don't know if i
# need to do a flaskform or if i can append html to the page using the API request
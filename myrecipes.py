import os
from flask import Flask, render_template, request, flash, redirect, session, g, jsonify
from flask_debugtoolbar import DebugToolbarExtension
from sqlalchemy.exc import IntegrityError
from forms import UserLoginForm, UserAddForm, UserEditForm
from models import db, connect_db, User, Collections, Recipe

# python3 -m venv venv
# source venv/bin/activate
# pip3 install -r dependencies.txt
# python3 -m app.py


CURR_USER_KEY = "curr_user"

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
    'DATABASE_URL', 'postgresql:///myrecipes')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'myrecipes')
toolbar = DebugToolbarExtension(app)

connect_db(app)

# User Routes
@app.before_request
def add_user_to_g():
    if CURR_USER_KEY in session:
        g.user = User.query.get_or_404(session[CURR_USER_KEY])
    else:
        g.user = None

def do_login(user):
    session[CURR_USER_KEY] = user.id

def do_logout():
    if CURR_USER_KEY in session:
        del session[CURR_USER_KEY]

@app.route('/')
def route():
    if g.user:
        return redirect(f'/users/home/{g.user.id}')

    return redirect('/welcome')

@app.route('/welcome')
def homepage():
    return render_template('/welcome.html')

@app.route('/signup', methods=["GET", "POST"])
def signup():

    if g.user:
        return redirect(f'/users/home/{g.user.id}')
        # return redirect(f'/users/{g.user.id}')

    form = UserAddForm()

    if form.validate_on_submit():
        try:
            user = User.signup(
                first_name=form.first_name.data,
                last_name=form.last_name.data,
                username=form.username.data,
                password=form.password.data,
                email=form.email.data,
            )
            db.session.commit()
        except IntegrityError:
            flash("Username already taken", 'danger')
            return render_template('users/signup.html', form=form)
        
        do_login(user)
        return redirect('/')
    else:
        return render_template('users/signup.html', form=form)

@app.route('/login', methods=["GET", "POST"])
def login():
    form = UserLoginForm()
    if form.validate_on_submit():
        user = User.authenticate(
            username=form.username.data,
            password=form.password.data
        )
        if user:
            do_login(user)
            flash(f"Hello, {user.username}!", "success")
            return redirect('/')
        flash("Invalid credentials", 'danger')

    return render_template('users/login.html', form=form)
    
@app.route('/logout')
def logout():
    do_logout()
    flash("You have successfully logged out", "success")
    return redirect('/login')

# Personal Contact Information
@app.route('/about')
def about():
    return render_template('about.html')
@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/users/home/<int:user_id>')
def home(user_id):
    user = User.query.get_or_404(user_id)
    return render_template('users/home.html', user=user)

@app.route('/users/test')
def test():
    return render_template('users/home.html')

@app.route('/users/search/<int:user_id>', methods=["GET", "POST"])
def search(user_id):
    user = User.query.get_or_404(user_id)
    return render_template('users/search.html', user=user)





@app.route('/users/collections/<int:user_id>', methods=["GET"])
def collections(user_id):

    user = User.query.get_or_404(user_id)
    
    return render_template('users/collections.html', user=user)



@app.route('/users/<int:user_id>/edit', methods=["GET", "POST"])
def edit_user(user_id):
    if g.user.id == user_id:
        user = User.query.get_or_404(user_id)
        form = UserEditForm(obj=user)
        if form.validate_on_submit():
            user.username = form.username.data
            user.email = form.email.data
            user.first_name = form.first_name.data
            user.last_name = form.last_name.data
            db.session.commit()
            return redirect(f'/users/{user_id}')
        else:
            return render_template('users/edit_user.html', form=form, user=user)
    else:
        flash("You do not have permission to do that", "danger")
        return redirect('/')
    
@app.route('/users/<int:user_id>/delete', methods=["POST"])
def delete_user(user_id):
    if g.user.id == user_id:
        do_logout()
        user = User.query.get_or_404(user_id)
        db.session.delete(user)
        db.session.commit()
        return redirect('/login')
    else:
        flash("You do not have permission to do that", "danger")
        return redirect('/')
    
@app.route('/users/add_collection/<input>', methods=["POST"])
def add_collection(input):
    try: 
        new_collection = Collections(title=input, user_id=g.user.id)
        db.session.add(new_collection)
        db.session.commit()
        return jsonify({"success": True})
    except:
        return jsonify({"success": False})
    # db.execute(""" INSERT INTO collections (title, user_id) VALUES (%s, %s);""", (input, g.user.id))

@app.route('/users/add_recipe/')
def add_recipe():
    try:
        new_recipe = Recipe(
            title=request.json.get('title'),
            ingredients=request.json.get('ingredients'),
            instructions=request.json.get('instructions'),
            image=request.json.get('image'),
            user_id=g.user.id
        )
        db.session.add(new_recipe)
        db.session.commit()
        return jsonify({"success": True})
    except:
        return jsonify({"success": False})
        
            
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        app.run(debug=True, port=8000)

"""Server for movie ratings app."""

from flask import (Flask, render_template, request, flash, session,
                   redirect)
from model import connect_to_db
import crud
from jinja2 import StrictUndefined
app = Flask(__name__)
app.secret_key = 'super secret key'
app.jinja_env.undefined = StrictUndefined


app = Flask(__name__)


@app.route('/')
def homepage():
    """View homepage."""

    return render_template('homepage.html')

@app.route("/movies")
def all_movies():
    """View all movies."""

    movies = crud.get_movies()

    return render_template("all_movies.html", movies=movies)
    
@app.route("/movies/<movie_id>")
def show_movie(movie_id):
    movie = crud.get_movie_by_id(movie_id)
    return render_template("movie_details.html", movie=movie)

@app.route("/movies/<movie_id>/rate")
def rate_movie(movie_id):
    score = request.args.get("rate")
    email = session.get('current_user')
    user = crud.get_user_by_email(email)
    movie = crud.get_movie_by_id
    crud.create_rating(user, int(score), movie)

        
    return render_template("movie_ratings.html")

@app.route("/users")
def all_users():
    users = crud.get_users()
    return render_template("all_users.html", users=users)

@app.route("/users", methods=["POST"])
def register_user():
    email = request.form.get("email")
    password = request.form.get("password")
    
    user = crud.get_user_by_email(email)
    if user:
        flash("Cannot create an account with that email because it is already in use. Try again.")
    else:
        crud.create_user(email, password)
        flash("Account created! Please log in.")
        
    return redirect ("/")

@app.route("/login", methods=["POST"])
def current_user():
    email = request.form.get("email")
    password = request.form.get("password")
    user = crud.get_user_by_email(email)
    if user.password == password:
        session['current_user'] = user.email
        flash('Logged in!')
        return redirect ("/")

if __name__ == "__main__":
    # DebugToolbarExtension(app)
    connect_to_db(app)
    app.secret_key = 'super secret key'
    app.run(host="0.0.0.0", debug=True)

import os

from cs50 import SQL
import requests
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required

# Configure application
app = Flask(__name__)
    
headers = {
        "accept": "application/json",
        'Content-Type': 'application/json', 
        "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiIzNGE2Mzg3MjYzYmU4YWFkODNhZGU1ZTA5YjVjNGRiZCIsInN1YiI6IjY1MDkwMzViMzk0YTg3MDExYzllNmM1NCIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.An03Ut_9kl-VT8pNRJ83oUajfz0N8SeJu1Cq6zV53EM"
}

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///users.db")

@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# Home page
@app.route("/")
@login_required
def index():
    """Show all the movies"""
     # Fetch trending movies and TV shows from an external API
    trending_all_url = "https://api.themoviedb.org/3/trending/all/day?language=en-US"
    trending_movie_url = "https://api.themoviedb.org/3/trending/movie/day?language=en-US"
    trending_tv_url = "https://api.themoviedb.org/3/trending/tv/day?language=en-US"

   
    try:
        trending_all = requests.get(trending_all_url, headers=headers)
        trending_movie = requests.get(trending_movie_url, headers=headers)
        trending_tv =requests.get(trending_tv_url, headers=headers)

        # check if all requests were successful ( 200 )
        if (trending_all.status_code == 200
            and trending_movie.status_code == 200 
            and trending_tv.status_code == 200):
                trending_all_data = trending_all.json()
                trending_movie_data = trending_movie.json()
                trending_tv_data = trending_tv.json()
                return render_template("index.html", trending_all=trending_all_data, trending_movie=trending_movie_data, trending_tv=trending_tv_data)

        else: 
            return "One or more API requests failed"
    except Exception as e:
        return f"An error occurred: {str(e)}"

# Define a route to display a list of movies
@app.route("/movies", methods=["GET", "POST"])
@login_required
def movies():
    """movies lists"""
    # Define the URL to fetch a list of movies from an external API
    movies_url = "https://api.themoviedb.org/3/discover/movie?include_adult=false&include_video=false&language=en-US&page=1&sort_by=popularity.desc"
    try:
        # Send a GET request to the API to fetch movies
        movies = requests.get(movies_url, headers=headers)
        # if request success
        if movies.status_code == 200:
            # Parse the JSON response
            movies_data = movies.json()
            return render_template("movies.html", movies_data= movies_data)
        else:
            return apology("Request failed")
    except Exception as e:
        return apology(f"An error occured: {str(e)}")

# Define a route to handle loading more movie data
@app.route("/load-more-data", methods=["GET"])
def load_more_data():
    try:
        # Get the requested page number from the query parameters
        page = int(request.args.get("page", 1))
                   
        # Define the URL to fetch more movie data based on the requested page
        more_movies_url = f"https://api.themoviedb.org/3/discover/movie?&include_adult=false&include_video=false&language=en-US&page={page}&sort_by=popularity.desc"
        more_movies = requests.get(more_movies_url, headers=headers)
        if more_movies.status_code == 200:
            more_movies_data = more_movies.json()
            
            return more_movies_data
        else:
            return apology("Request Failed! ")  

    except Exception as e:
        return apology(f"An error occured: {str(e)}")

# Define a route to display a list of TV series
@app.route("/tv-series")
@login_required
def tv_series():
    """tv series list"""
    # Define the URL to fetch a list of TV series from an external API
    tv_url = "https://api.themoviedb.org/3/discover/tv?include_adult=false&include_video=false&language=en-US&page=1&sort_by=popularity.desc"
    try:
        # fetch the data.
        tv = requests.get(tv_url, headers=headers)
        if tv.status_code == 200:
            # return JSON
            tv_data = tv.json()
            return render_template("tv-series.html", tv_data= tv_data)
        else:
            return apology("Requet Failed!")
    except Exception as e:
         return apology(f"An error occured: {str(e)}")

# load more movies request handler.
@app.route("/load-more-data-tv", methods=["GET"])
def load_more_data_tv():
    try:
        # get the requested page number
        page = int(request.args.get("page", 1))
        
        more_tv_url = f"https://api.themoviedb.org/3/discover/tv?&include_adult=false&include_video=false&language=en-US&page={page}&sort_by=popularity.desc"
        more_tv = requests.get(more_tv_url, headers=headers)
        if more_tv.status_code == 200:
            more_tv_data = more_tv.json()
            
            return more_tv_data
        else:
            return apology("Request Failed! ")  

    except Exception as e:
        return apology(f"An error occured: {str(e)}")

@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")

@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")

# regieter route    
@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "POST":
        # get the data from userinputs
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")
        database_username = db.execute(
            "SELECT * FROM users WHERE username = ?", username.lower()
        )

        # check the possible errors
        if not username or not password or not confirmation:
            return apology("please fill the inputs")
        elif password != confirmation:
            return apology("password do not match")
        elif database_username:
            return apology("username is already taken")
        else:
            # hashed password and store in db.
            hashed_password = generate_password_hash(password, method="sha256")
            db.execute(
                "INSERT INTO users (username, hash) VALUES (? , ? )",
                username,
                hashed_password,
            )
            id = db.execute("SELECT * FROM users WHERE username = ?", username)
            session["user_id"] = id[0]["id"]
            return redirect("/")

    else:
        return render_template("register.html")

# Define a route to display and update the user's account information
@app.route("/account", methods=["GET", "POST"])
@login_required
def account():
    user = db.execute("SELECT * FROM users WHERE id = ?", session["user_id"])
    if request.method == "GET":
        return render_template("account.html",user=user[0]["username"])
    if request.method == "POST":
        old_password = request.form.get("cur_password")
        new_password = request.form.get("new_password")
        con_password = request.form.get("confirmation")

        if not old_password or not new_password or not con_password:
            return apology("Inputs must not be empty!")
        
        elif len(user) != 1 or not check_password_hash(user[0]["hash"], old_password):
            return apology("invalid username and/or password", 403)
        
        elif new_password != con_password:
            return apology("Password do not match!")
        
        else:
            hashed_password = generate_password_hash(con_password, method="sha256")
            db.execute("UPDATE users SET hash = ? WHERE id = ?",
                       hashed_password,
                       session["user_id"]
            )
            return redirect("/")

# Define a route to search for movies or TV series
@app.route("/search", methods=["GET"])
def search():
    try:
        # Get the search query from the request
        title = request.args.get("query")

        # Define the URL to search for movies or TV series based on the query
        url = f"https://api.themoviedb.org/3/search/multi?query={title}&include_adult=false&language=en-US&page=1"
        search_result = requests.get(url, headers=headers)
        if search_result.status_code == 200:    
            search_result_data = search_result.json()
            return search_result_data
        else:
            return apology("Not found !")
    
    except Exception as e:
        return apology(f"An error occured: {str(e)}")


# Define a route to display details of a specific movie
@app.route("/details", methods=["GET"])
def details():
    try:
        # Get the target movie ID from the request
        target_id = int(request.args.get("target"))
        details_url = f"https://api.themoviedb.org/3/movie/{target_id}" 

        details = requests.get(details_url, headers=headers)

        if details.status_code == 200:
            details_data = details.json()
            return render_template("details.html", details_data=details_data) 
        else:
            return apology("not found!")
        
    except Exception as e:
        return apology(f"an error occured: {str(e)}")

@app.route("/details-tv", methods=["GET"])
def details_tv():
    try:
        tv_id = int(request.args.get("tv_id"))
        tv_url = f"https://api.themoviedb.org/3/tv/{tv_id}?language=en-US"

        tv = requests.get(tv_url, headers=headers)  

        if tv.status_code == 200:
            tv_data = tv.json()
            return render_template("tv.html", tv_data=tv_data)
        else:
            return apology("not found!")
    except Exception as e:
        return apology(f"an error occured: {str(e)}")

@app.route("/saved-movie", methods=["GET","POST"])
def saved():
    
    if request.method == "POST":
        movie_id = request.json.get("movieId")
        type = request.json.get("type")
        
        if movie_id and type:
            # Insert the movie or TV series into the favorites table for the current user
            db.execute("INSERT INTO favorites (user_id, movie_id, type) VALUES (?, ?, ?)",session["user_id"], movie_id, type)
            return redirect("saved-movie")
        else:
            return apology("movie does not exist")
    
    else:
        # Retrieve the user's saved movies and TV series from the database
        data = db.execute("SELECT * FROM favorites WHERE user_id = ?", session["user_id"] )
        fav = []
        for data in data:
            if data["type"] == "movie":
                url = f"https://api.themoviedb.org/3/movie/{data['movie_id']}"
                movies_url = requests.get(url, headers=headers)
                fav.append(movies_url.json())
                   
            else:
                url = f"https://api.themoviedb.org/3/tv/{data['movie_id']}?language=en-US"
                tv_url = requests.get(url, headers=headers)
                fav.append(tv_url.json())

        return render_template("saved.html", data=fav)  
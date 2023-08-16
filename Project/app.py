from cs50 import SQL
from flask import Flask, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime
from helpers import login_required, sulogin_required

# Configure application
app = Flask(__name__)

# Configure Session
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.config["TEMPLATES_AUTO_RELOAD"] = True
Session(app)

# Open the database
db = SQL("sqlite:///store.db")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
@login_required
def index():
    """Show all items"""
    
    # TODO: pass items to render_template
    return render_template("index.html")


@app.route("/item", methods=["GET"])
@login_required
def item():
    """Show individual item"""

    # TODO

    return render_template("item.html")


@app.route("/cart")
@login_required
def cart():
    """Show items in cart"""

    # TODO

    return render_template("cart.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """ Register a user"""

    # TODO: User reached route via POST (submitted a form)
    if request.method == "POST":
        ...
    
    # TODO: User reached route via GET (clicked on a link, redirected or typed this route)
    else:
        return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    """ Log user in"""

    # TODO: Forget any user_id

    # TODO: User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        ...
    
    # TODO: User reached route via GET (as by clicking a link or via a redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    "Log user out"

    # TODO
    ...


@app.route("/account")
@login_required
def account():
    """Show user his account"""
    
    # TODO

    return render_template("account.html")


@app.route("/sulogin", methods=["GET", "POST"])
def sulogin():
    """ Log superuser in"""

    # TODO: Forget any su_id

    # TODO: User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        ...
    
    # TODO: User reached route via GET (as by clicking a link or via a redirect)
    else:
        return render_template("sulogin.html")


@app.route("/sulogout")
def sulogout():
    "Log superuser out"

    # TODO
    ...


@app.route("/suaccount")
@sulogin_required
def suaccount():
    """Show superuser his account"""
    
    # TODO: Only allow to change passwords

    return render_template("account.html")

@app.route("/su")
@sulogin_required
def su():
    """Show admin panel"""

    # TODO

    return render_template("su.html")


@app.route("/suitems")
@sulogin_required
def su_items():
    """Show list of buyable items to admin"""

    # TODO

    return render_template("suitems.html")
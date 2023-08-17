import ast
from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
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

    # Query database for items
    rows = db.execute("SELECT * FROM items")

    return render_template("index.html", items=rows)


@app.route("/item/<id>", methods=["GET"])
@login_required
def item(id):
    """Show individual item"""

    rows = db.execute("SELECT * FROM items WHERE id = ?", id)

    return render_template("item.html", item=rows[0])


@app.route("/cart", methods=["GET", "POST"])
@login_required
def cart():
    """Show items in cart"""

    # User reached route via POST (submitted a form)
    if request.method == "POST":
    
        # Add this item to user's cart IF it exists
        item_id = request.form.get("id")
        try:
            quantity = int(request.form.get("qty"))
        except ValueError:
            flash("An error occurred.")
            return redirect("/")

        if item_id and request.form.get("qty"):

            rows = db.execute("SELECT * FROM cart WHERE item_id = ? AND user_id = ?",
            item_id, session["user_id"])
            if len(rows) > 0:
                try:
                    current_quantity = int(rows[0]["quantity"])
                except ValueError:
                    flash("An error occurred.")
                    return redirect("/")
                
                db.execute("UPDATE cart SET quantity = ? WHERE item_id = ? AND user_id = ?",
                current_quantity + quantity, item_id, session["user_id"])
            else:
                db.execute("INSERT INTO cart (user_id, item_id, quantity) VALUES (?, ?, ?)",
                session["user_id"], item_id, quantity)

    # Select items from user's cart
    cart = db.execute("SELECT * FROM cart JOIN items ON items.id = cart.item_id WHERE cart.user_id = ?", session["user_id"])

    total = 0.00
    for item in cart:
        total += item["price"] * item["quantity"]

    # Pass user's cart items to cart route
    return render_template("cart.html", cart=cart, total=total)


@app.route("/update", methods=["POST"])
def update():
    """Update an item's quantity"""
    
    item_id = request.form.get("id")
    try:
        quantity = int(request.form.get("qty"))
    except ValueError:
        flash("An error occurred.")
        return redirect("/")

    if item_id and quantity:
        db.execute("UPDATE cart SET quantity = ? WHERE item_id = ? AND user_id = ?",
        quantity, item_id, session["user_id"])
        print(item_id, quantity)
    return redirect("/cart")


@app.route("/delete", methods=["POST"])
def delete():
    """Delete an item from cart"""

    try:
        item_id = int(request.form.get("id"))
    except ValueError:
        flash("An error occurred.")
        return redirect("/")
    
    if item_id:
        db.execute("DELETE FROM cart WHERE item_id = ? AND user_id = ?",
        item_id, session["user_id"])
    return redirect("/cart")


@app.route("/checkout", methods=["POST"])
def checkout():
    """Check user out"""
    
    items = request.form.get("checkout")
    if items:
        flash("Thank you! Please await the delivery.", "info")
        items = ast.literal_eval(items)
        for item in items:
            db.execute("INSERT INTO orders (user_id, item_id, quantity, date) VALUES(?, ?, ?, ?)",
                session["user_id"], item["item_id"], item["quantity"], datetime.now())
        db.execute("DELETE FROM cart WHERE user_id = ?", session["user_id"])
    return redirect("/")


@app.route("/register", methods=["GET", "POST"])
def register():
    """ Register a user"""

    # User reached route via POST (submitted a form)
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        # Ensure user provided username, password, confirmation
        if not username:
            flash("Username is required.", "info")
            return render_template("register.html")

        elif not password:
            flash("Password is required.", "info")
            return render_template("register.html")

        elif not confirmation or password != confirmation:
            flash("Passwords do not match.", "info")
            return render_template("register.html")
        
        elif len(password) < 8:
            flash("Password needs to be at least 8 characters.", "info")
            return render_template("register.html")


        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", username)

        # Ensure the username is not taken
        if len(rows) == 1:
            flash("Username is taken", "info")
            return render_template("register.html")

        # INSERT the new user into users table, storing a hash of user's password
        db.execute("INSERT INTO users (username, hash) VALUES (?, ?)",
        username, generate_password_hash(password))

        # Redirect the user to login page
        return redirect("/login")
    
    # User reached route via GET (clicked on a link, redirected or typed this route)
    else:
        return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    """ Log user in"""

    # Forget any user_id
    session.clear()

    #  User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        
        username = request.form.get("username")
        password = request.form.get("password")

        # Ensure user provided username and password
        if not username:
            flash("Username is required.", "info")
            return render_template("login.html")

        elif not password:
            flash("Password is required.", "info")
            return render_template("login.html")
        
        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", username)

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], password):
            flash("Invalid username and/or password.", "info")
            return render_template("login.html")
        
        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to index
        return redirect("/")

    
    # User reached route via GET (as by clicking a link or via a redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    "Log user out"

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


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
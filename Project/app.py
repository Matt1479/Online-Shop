import os
import ast
from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import secure_filename
from datetime import datetime
from helpers import login_required, sulogin_required, allowed_file, usd

UPLOAD_FOLDER = 'static/images'

# Configure application
app = Flask(__name__)

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure Session
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
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


@app.route("/search")
def search():
    """Search for an item by title"""

    query = request.args.get("q")

    if query:
        items = db.execute("SELECT * FROM items WHERE title LIKE ? LIMIT 15", "%" + query + "%")
    else:
        items = []
    
    # Return list of items in JSON format
    return jsonify(items)


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


@app.route("/orders")
@login_required
def orders():
    """Show user his orders"""
    
    rows = db.execute("SELECT * FROM orders JOIN items ON items.id = orders.item_id WHERE orders.user_id = ?",
    session["user_id"])

    return render_template("orders.html", orders=rows)


@app.route("/sulogin", methods=["GET", "POST"])
def sulogin():
    """ Log superuser in"""

    # Forget any su_id
    session.clear()

    #  User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        
        username = request.form.get("username")
        password = request.form.get("password")

        # Ensure user provided username and password
        if not username:
            flash("Username is required.", "info")
            return render_template("sulogin.html")

        elif not password:
            flash("Password is required.", "info")
            return render_template("sulogin.html")
        
        # Query database for username
        rows = db.execute("SELECT * FROM su WHERE username = ?", username)

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], password):
            flash("Invalid username and/or password.", "info")
            return render_template("sulogin.html")
        
        # Remember which user has logged in
        session["su_id"] = rows[0]["id"]

        # Redirect user to index
        return redirect("/su")

    
    # User reached route via GET (as by clicking a link or via a redirect)
    else:
        return render_template("sulogin.html")


@app.route("/sulogout")
def sulogout():
    "Log superuser out"

    # Forget any su_id
    session.clear()

    # Redirect su to login form
    return redirect("/sulogin")


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

    pending = db.execute("SELECT *, orders.id as order_id FROM orders JOIN items ON items.id = orders.item_id WHERE orders.status = 'pending'")
    sent = db.execute("SELECT *, orders.id as order_id FROM orders JOIN items ON items.id = orders.item_id WHERE orders.status = 'sent'")
    delivered = db.execute("SELECT *, orders.id as order_id FROM orders JOIN items ON items.id = orders.item_id WHERE orders.status = 'delivered'")
    cancelled = db.execute("SELECT *, orders.id as order_id FROM orders JOIN items ON items.id = orders.item_id WHERE orders.status = 'cancelled'")

    statuses = ['pending', 'sent', 'delivered', 'cancelled']

    return render_template("su.html",
        pending=pending,
        sent=sent,
        delivered=delivered,
        cancelled=cancelled, 
        statuses=statuses)


@app.route("/updatestatus", methods=["GET", "POST"])
@sulogin_required
def updatestatus():
    """Update status of an item"""

    if request.method == "POST":
        order_id = request.form.get("order_id")
        status = request.form.get("status")

        if status and order_id:
            db.execute("UPDATE orders SET status = ? WHERE id = ?",
            status, order_id)
        
        return redirect("/su")

    else:
        return redirect("/su")


@app.route("/suitems")
@sulogin_required
def su_items():
    """Show list of items that users can buy"""

    rows = db.execute("SELECT * FROM items")

    return render_template("suitems.html", items=rows)


@app.route("/suedititem/<int:id>", methods=["GET", "POST"])
@sulogin_required
def suedititem(id):
    """Edit an item"""

    if request.method == "POST":

        title = request.form.get("title")
        price = request.form.get("price")
        description = request.form.get("description")

        if title and price and description:
            db.execute("UPDATE items SET title = ?, price = ?, description = ? WHERE id = ?",
            title, price, description, id)

        return redirect("/suitems")

    else:

        rows = db.execute("SELECT * FROM items WHERE id = ?", id)

        return render_template("edit.html", item=rows[0])


@app.route("/sudeleteitem", methods=["POST"])
@sulogin_required
def sudeleteitem():
    """Delete a buyable item from the database"""

    item_id = request.form.get("id")

    if item_id:
        rows = db.execute("SELECT image_path as path FROM items WHERE id = ?", item_id)
        db.execute("DELETE FROM items WHERE id = ?", item_id)
        os.remove(os.path.join(rows[0]["path"]))


    return redirect("/suitems")

@app.route("/sunewitem", methods=["GET", "POST"])
@sulogin_required
def sunewitem():
    """Add a new item to the shop"""

    if request.method == "POST":
        title = request.form.get("title")
        price = request.form.get("price")
        description = request.form.get("description")

        if title and price and description:
            # check if the post request has the file part
            if 'file' not in request.files:
                flash('No file part')
                return redirect(request.url)
            file = request.files['file']
            # if user does not select file, browser also
            # submit a empty part without filename
            if file.filename == '':
                flash('No selected file')
                return redirect(request.url)
            if file and allowed_file(file.filename):
                filename, extension = secure_filename(file.filename), os.path.splitext(file.filename)

                cur_id = db.execute("SELECT MAX(id) as cur_id FROM items")
                new_id = int(cur_id[0]["cur_id"] + 1)
                new_name = str(new_id) + extension[1]

                file.save(os.path.join(app.config['UPLOAD_FOLDER'], new_name))
            
            db.execute("INSERT INTO items (title, image_path, price, description) VALUES (?, ?, ?, ?)",
            title, (UPLOAD_FOLDER + '/' + new_name), price, description)

        else:
            flash("Missing title, price, or description.")
            return redirect("/sunewitem")
        
        return redirect("/suitems")
    
    else:
        return render_template("new.html")
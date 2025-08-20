# Online Shop

> See a remake of this project that uses SQLite3 instead of CS50.SQL: https://github.com/Matt1479/Online-Shop-Remake

#### Video Demo: https://youtu.be/qeWnnzCsNBA

#### Description
Welcome! This project is a web store, it's written in Python using the Flask framework. It allows users to create an account, purchase various items, view their orders and more. I hope you'll like it!

#### Getting Started - Installation
- Clone this repository: `git clone https://github.com/Matt1479/Online-Shop`
- Install dependencies by running  `pip install -r requirements.txt`

#### How to use this Project
- Run the application using: `flask run`
- Click on the link provided by the CLI. You should be welcomed by the login page.
- Feel free to create an account, buy some items, view your orders, etc.
    - If you'd like to use the admin panel, navigate to `/su` , you should be welcomed by the superuser login page.
        - The credentials are as follows:
            - login: `testsu`
            - password: `cs50`
        - In there you can view orders made by users, see the item panel, etc.

#### Features
- User panel:
    1. Login and Register.  
    <img src="screenshots/0.login.png">  
    <img src="screenshots/1.register.png">  
    2. Change user's password.  
    <img src="screenshots/6.changepassword.png">  
    3. View available items to buy.  
    <img src="screenshots/2.index.png">  
    4. Search for an item through a search bar.  
    <img src="screenshots/2.index.search.png">  
    5. View an item, change item's quantity, add to cart.  
    <img src="screenshots/3.item0.png">  
    <img src="screenshots/3.item1.png">  
    <img src="screenshots/3.item2.png">  
    6. View cart, change item's quantity in cart, delete an item from cart, checkout/buy all items in a cart.  
    <img src="screenshots/4.cart0.png">  
    <img src="screenshots/4.cart1.png">  
    <img src="screenshots/4.cart0.png">  
    <img src="screenshots/4.cart2.png">  
    <img src="screenshots/4.cart3.png">  
    <img src="screenshots/5.checkout.png">  
    7. View user's orders (name, price, quantity, status, date)  
    <img src="screenshots/7.orders.png">  

- Admin panel:
    1. View orders and change their respective statuses (pending, sent, delivered, or cancelled).  
    <img src="screenshots/8.sulogin.png">  
    <img src="screenshots/9.su.png">  
    <img src="screenshots/10.itemstatus0.png">  
    <img src="screenshots/10.itemstatus1.png">  
    2. View, Edit, or Delete items that are available to buy in the shop.  
    <img src="screenshots/12.edit0.png">  
    <img src="screenshots/12.edit1.png">  
    <img src="screenshots/12.edit2.png">  
    <img src="screenshots/13.delete.png">  
    3. Add new items to the shop.  
    <img src="screenshots/14.newitem0.png">  
    <img src="screenshots/14.newitem1.png">  
    4. 404 page.  
    <img src="screenshots/15.notfound.png">  

#### Technologies used:
- Python
- Flask
- Jinja
- sqlite3
- HTML, CSS, JavaScript, AJAX
- Bootstrap
- And other small modules (libraries)

#### References
- [Python3 documentation](https://www.python.org/)
- [Flask documentation](https://flask.palletsprojects.com/en/2.3.x/)
- [Boostrap documentation](https://getbootstrap.com/)


#### License
This project is licensed under MIT license. See <a href="./LICENSE.md">LICENSE</a> file for more information.

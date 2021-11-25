from flask import Blueprint, json, make_response, abort, request, render_template
from flask.helpers import flash, url_for
from flask.wrappers import Request
from flask_cors import CORS
from sqlalchemy import engine
from sqlalchemy.sql import func
from sqlalchemy.sql.functions import user
from flask_login.utils import login_user, current_user
from werkzeug.security import generate_password_hash
from werkzeug.utils import redirect
from Website import create_app
from .models import Orders
from .models import design as Design
from .models import User, Colors, Client
from . import DB_NAME, db
from datetime import date

views = Blueprint('views', __name__)


@views.route('/create_order', methods=["GET", "POST"])
def create_order():
    designs = Design.query.all()
    colors = Colors.query.all()

    if request.method == "GET":
        db.create_all()
        for design in designs:
            """ This will make every type of (shirt, hoodie) in the list as an independent value 
            Format in database must be like: 'Shirt hoodie cap ....' with a space between every
            type and the other.  """

            product_type = list(design.Type.split(" "))

        if current_user.is_authenticated:
            return render_template('create_order.html', designs=designs, colors=colors, user=current_user,
            product_type=product_type)
        else:
            return redirect(url_for('auth.login'))

    elif request.method == "POST":
        """ same as the one at the GET, to avoid 'UnboundLocalError: local variable 
        'product_type' referenced before assignment'
         """

        for design in designs:
            product_type = list(design.Type.split(" "))

        design = request.form.get('design')
        size = request.form.get('size')
        quantity = request.form.get('quantity')
        color = request.form.get('color')
        adjustment = request.form.get('adjustment')
        client_phone = request.form.get('client_phone')
        product = request.form.get('Type')
        author = current_user.username
        client = Client().query.filter_by(client_phone_number=client_phone).first()
        new_shirt = Orders(design_name=design, tshirt_size=size, quantity=quantity,
                           color=color, adjustments=adjustment, client_number=client_phone,
                           Type=product, author=author)

        if client_phone == '':
            flash("Please enter client's phone number!", category='error')

        elif len(client_phone) < 9:
            flash("Phone number must be 9 numbers!", category='error')

        elif not client:
            flash("Must add client first!", category='error')

        elif product == "Choose a product":
            flash("Please choose a product!", category='error')

        else:
            try:
                int(client_phone)
                
                """
                    checking if same order already exists and if so
                    it will add quantit to the existing order else will
                    add a new shirt to the database.
                """
                client_order = Orders().query.filter_by(
                design_name=design, 
                color=color,
                tshirt_size=size,
                adjustments=adjustment,
                Type=product,
                author=author,
                date=date.today(),
                done=False).first()

                design = Design.query.filter_by(name=design).first()
                if client_order:

                    client_order.quantity += int(quantity)
                    design.sold += int(quantity)
                    db.session.commit()

 

                elif not client_order:
                    db.session.add(new_shirt)
                    design.sold += int(quantity)
                    db.session.commit()

                # It's kinda obvius .... 
                def totalPrice(new_shirt):
                    
                    shirtPrice = (int(quantity)*design.shirt_price)
                    hoodiePrice = (int(quantity)*design.hoodie_price)
                    tax = 0.15

                    if new_shirt.Type == 'Shirt':
                        total_price = f"Total price: {shirtPrice*tax+shirtPrice}" 

                    
                    elif new_shirt.Type == 'Hoodie':
                        total_price = f"Total price: {hoodiePrice*tax+hoodiePrice}"

                    flash(f"Order created! {total_price}", category="success")

                totalPrice(new_shirt)
            except ValueError:
                flash("Phone number can only be numbers!", category='error')


            return render_template('create_order.html', designs=designs, colors=colors, user=current_user,
            product_type=product_type)

    return render_template('create_order.html', designs=designs, colors=colors, user=current_user,
    product_type=product_type)



@views.route('/register_client', methods=["GET", "POST"])
def register_client():
    if request.method == "GET":
        if current_user.is_authenticated:
            return render_template('client.html')
        else:
            return redirect(url_for('auth.login'))

    if request.method == "POST":
        firstName = request.form.get("firstName")
        lastName = request.form.get("lastName")
        city = request.form.get("city")
        distruct = request.form.get("distruct")
        client_phone = request.form.get("phoneNumber")
        client = Client().query.filter_by(client_phone_number=client_phone).first()


        if not client:
            if len(firstName) < 3:
                flash("First name should be more than 2 characters!", category='error')
            if len(lastName) < 3:
                flash("Last name should be more than 2 characters!", category='error')
            if client_phone == '':
                flash("Please enter client's phone number", category='error')
            if len(client_phone) < 9:
                flash("Phone number has to be 9 characters", category='error')
            try:
                int(client_phone)
            except ValueError:
                flash("Phone number can only be numbers!", category='error')

            else:
                new_client = Client(client_first_name=firstName, client_last_name=lastName, client_city=city,
                client_distruct=distruct, client_phone_number=client_phone,
                added_by=current_user.username)
                db.session.add(new_client)
                db.session.commit()
                flash("Client added successfully!",category="success")
        else:
            flash("Client already exists!", category="error")


    return render_template('client.html')

@views.route('/', methods=["GET", "POST"])
def index():

    if not current_user.is_authenticated:
        return redirect(url_for('auth.login'))
    
    return redirect(url_for('views.register_client'))


@views.route('/orders', methods=["GET", "POST"])
def orders():

    if request.method == "POST":
        client_number = request.form.get("phoneNumber")
        orders = Orders.query.filter_by(client_number=client_number).all()
        client = Client.query.filter_by(client_phone_number=client_number).first()

        return render_template("orders.html", orders=orders,client=client)
    return render_template("orders.html")
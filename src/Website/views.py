from flask import Blueprint, json, make_response, abort, request, render_template
from flask.helpers import flash, url_for
from flask.wrappers import Request
from flask_cors import CORS
from sqlalchemy import engine
from sqlalchemy.sql.functions import user
from flask_login.utils import login_user, current_user
from werkzeug.security import generate_password_hash
from werkzeug.utils import redirect
from Website import create_app
from .models import Orders as Orders, User, Colors, Client
from .models import design as Design
from . import DB_NAME, db
views = Blueprint('views', __name__)


@views.route('/create_order', methods=["GET", "POST"])
def create_order():
    designs = Design.query.all()
    colors = Colors.query.all()

    if request.method == "GET":
        for color in colors:
            """ This will make ever Size in the list as an independent value 
                Format in database must be like: 'S M L XL ....' with a space between every
                size and the other.  """

            color = list(color.available_size.split(" "))

        if current_user.is_authenticated:
            return render_template('create_order.html', designs=designs, colors=colors, color=color, user=current_user)
        else:
            return redirect(url_for('auth.login'))

    elif request.method == "POST":

        for color in colors:
            db_color = list(color.available_size.split(" "))
        design = request.form.get('design')
        size = request.form.get('size')
        quantity = request.form.get('quantity')
        color = request.form.get('color')
        adjustment = request.form.get('adjustment')
        client_phone = request.form.get('client_phone')
        author = current_user.username
        client = Client().query.filter_by(client_phone_number=client_phone).first()

        new_shirt = Orders(design_name=design, tshirt_size=size, quantity=quantity,
                           color=color, adjustments=adjustment, client_number=client_phone, author=author)


        if client_phone == '':
            flash("Please enter client's phone number!", category='error')
        try:
            int(client_phone)
        except ValueError:
            flash("Phone number can only be numbers!", category='error')



        else:
            try:




                """ This code keeps returning 'Can't Operate on a closed database' So
                basically it gives an error ever time someone adds a shirt. Couldn't 
                solve this at the moment. """

                shirts = db.session.execute(
                    f'SELECT * From Orders WHERE design_name="{design}" AND color="{color}" AND author="{author}" AND client_number="{client_phone}" AND tshirt_size="{size}"')

                """looping throught all shirts in the db, compares it to the new one
                and if it exists it will the new quantity to the old one."""

                for shirt in shirts:
                    shirt['quantity'] + int(quantity)
                    shirt = Orders.query.filter_by(id=shirt['id']).first()
                    shirt.quantity += int(quantity)
                    design = Design.query.filter_by(name=design).first()
                    design.sold += int(quantity)
                    db.session.commit()
                    flash("Order created successfully!", category="success")


                # Adds incase it doesn't exist, somehow i can't make triple quotation :$
                else:
                    design = Design.query.filter_by(name=design).first()
                    design.sold += int(quantity)
                    db.session.add(new_shirt)
                    db.session.commit()
                    flash("Order created successfully!", category="success")


                    
            # SHUTUP I KNOW
            except Exception as e:
                print(e)


        return render_template('create_order.html', designs=designs, colors=colors, color=db_color, user=current_user)



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
            try:
                int(client_phone)
            except ValueError:
                flash("Phone number can only be numbers!", category='error')

            else:
                new_client = Client(client_first_name=firstName, client_last_name=lastName, client_city=city, client_distruct=distruct, client_phone_number=client_phone, added_by=current_user.username)
                db.session.add(new_client)
                db.session.commit()
                flash("Client added successfully!",category="success")
        else:
            flash("Client already exists!", category="error")


    return render_template('client.html')

@views.route('/', methods=["GET", "POST"])
def home():

    if not current_user.is_authenticated:
        return redirect(url_for('auth.login'))
    else:
        return redirect(url_for('views.register_client'))
from flask.helpers import flash, url_for
from flask_login.utils import login_user, current_user, logout_user, login_required
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import redirect
from . import db
from flask import Blueprint, json, make_response, abort, request
import flask
from flask import jsonify
from flask.templating import render_template
from flask_wtf.csrf import CSRFError
from .models import User, Colors
auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', "POST"])
def login():
    if request.method == "POST":
        username = request.form.get('username')
        password = request.form.get('password')

        """Instead of a sign up, i made this code to generate the new user to avoid sign up and
        i am too lazy to do it.
        """

        # new_user = User(username='dar3en', password=generate_password_hash(password, method='sha256'))
        # db.session.add(new_user)
        # db.session.commit()
        # flash("User created!", category='success')



        user = User.query.filter_by(username=username).first()
        
        if user:
            if check_password_hash(user.password, password):
                login_user(user, remember=True)
                return redirect(url_for('views.create_order'))
            else:
                flash("Wrong Password ! if you forgot the password please contact admin", category='error')
    
    return render_template('login.html', user=current_user)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/checkSizes/<color>', methods=["GET","POST"])
def check_sizes(color):
    sizes = Colors.query.filter_by(color=color).all()

    
    for size in sizes:
        Color = {
            'color': size.color,
            'sizes': size.available_size.split(" ")
        }

        

    return jsonify(Color)
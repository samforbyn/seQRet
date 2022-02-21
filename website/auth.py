from sqlite3 import IntegrityError
from unicodedata import category
from flask import Blueprint, redirect, render_template, request, flash, redirect, url_for
from flask_login import login_user, login_required, logout_user, current_user
from sqlalchemy.exc import IntegrityError
from .models import Users
from werkzeug.security import generate_password_hash, check_password_hash
from . import db 

auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = Users.query.filter_by(email=email).first()

        if user:
            if check_password_hash(user.password, password):
                flash("Logged in successfully!", category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.feed'))
            else:
                flash('Incorrect password, try again.', category='error')
        else:
            flash('No account with that email has been created', category='error')
    return render_template('login.html', user=current_user)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == "POST":
        first_name = request.form.get('firstName')
        last_name = request.form.get('lastName')
        username = request.form.get('username')
        email = request.form.get('email')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        user = Users.query.filter_by(email=email).first()

        if user:
            flash('An account with this email already exists, try again.', category='error')
        if len(email) < 3:
            flash('Your email needs to contain at least 3 characters, please try again.', category='error')
        elif len(first_name) < 1:
            flash('Your first name needs to contain more than 1 character, please try again.', category='error')
        elif len(last_name) < 1:
            flash('Your last name needs to contain more than 1 character, please try again.', category='error')
        elif len(username) < 4:
            flash('Your username needs to contain more than 3 character, please try again.', category='error')
        elif password1 != password2:
            flash('Passwords do not match, please try again.', category='error')
        elif len(password1) < 7:
            flash('Your password needs to contain at least 7 characters, try again.', category='error')
        else:
            new_user = Users(first_name=first_name, last_name=last_name, username=username, email=email, password=password1)
            print(new_user)
            db.session.add(new_user)
            try:
                db.session.commit()
            except IntegrityError as e:
                db.session.rollback()
                flash('Username already taken, try again.', category='error')
                return redirect(url_for('auth.sign_up', error=e))
            flash('Account created! You can log in now.', category='success')
            return redirect(url_for('views.home'))

    return render_template('sign_up.html', user=current_user)


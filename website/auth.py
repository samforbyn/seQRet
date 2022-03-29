from sqlite3 import IntegrityError
from flask import Blueprint, redirect, render_template, request, flash, redirect, url_for
from flask_login import login_user, login_required, logout_user, current_user
from sqlalchemy.exc import IntegrityError
from .models import Favorites, Users, Posts
from werkzeug.security import generate_password_hash, check_password_hash
from . import db, s3, BUCKET_NAME


auth = Blueprint('auth', __name__)


@auth.route('/')
@auth.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('views.home', user=current_user))

    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = Users.query.filter_by(email=email).first()
        
        if user:
            if check_password_hash(user.password, password):
                flash("Logged in successfully!", category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home', user=current_user))
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
    if current_user.is_authenticated:
        return redirect(url_for('views.home', user=current_user))

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
                return redirect(url_for('auth.sign_up'))
            flash('Account created!', category='success')
            this_user = Users.query.filter_by(email=email).first()
            login_user(this_user, remember=True)
            return redirect(url_for('views.home', user=current_user))

    return render_template('sign_up.html', user=current_user)

@auth.route('/profile', methods=['GET', 'POST'])
def profile():
    
    user = Users.query.filter_by(username=current_user.username).first()
    users_posts = Posts.query.filter_by(post_author=user.user_id).all()
    users_favorites = Favorites.query.filter_by(user_id=user.user_id).all()
    favorite_ids = [x.post_id for x in users_favorites]
    fav_posts = Posts.query.filter(Posts.post_id.in_(favorite_ids)).all()

    if request.method == 'POST':

        update = request.form.get('cpassword')
        newpass = request.form.get('newPassword')
        confirmpass = request.form.get('confirmPassword')

        if update:
            if check_password_hash(user.password, update):
                if len(newpass) < 7:
                    flash('Your password needs to contain at least 7 characters, try again.', category='error')
                    return redirect(url_for('auth.profile', user=current_user))
                if newpass != confirmpass:
                    flash('The two new password fields must match. Please try again.')
                    return redirect(url_for('auth.profile', user=current_user))
                user.password = generate_password_hash(password=confirmpass, method="sha256")
                db.session.commit()
                flash('Password changed successfully!', category='success')
            else:
                flash('The current password you entered is incorrect. Please try again.')

        see_more = request.form.get('seeMore')
        if see_more:
            return redirect(url_for('views.single_post', user=current_user, id = see_more))

        remove_post = request.form.get('removePost')
        if remove_post:
            selected = Posts.query.filter_by(post_id=remove_post).first()
            db.session.delete(selected)
            db.session.commit()
            
            users_posts = Posts.query.filter_by(post_author=user.user_id).all()
            users_favorites = Favorites.query.filter_by(user_id=user.user_id).all()
            favorite_ids = [x.post_id for x in users_favorites]
            fav_posts = Posts.query.filter(Posts.post_id.in_(favorite_ids)).all()

            s3.Object(BUCKET_NAME, selected.post_img).delete()

            flash('Post deemed not worthy of existing. It has been removed.')
            return render_template('profile.html', user=current_user, posts=users_posts, favorites=fav_posts)

    return render_template('profile.html', user=current_user, posts=users_posts, favorites=fav_posts)

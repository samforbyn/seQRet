from sqlite3 import IntegrityError
from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import login_required, current_user
import random
from .models import Posts, Favorites
from . import db


views = Blueprint('views', __name__)

@views.route('/home', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST':
        text = request.form.get('post_content')
        title = request.form.get('post_title')

        if len(title) <1:
            flash('Please enter a title', category='error')
        if len(text) < 1:
            flash('No text entered, try again.', category='error')
        else:
            user_text = Posts(post_title=title, post_content=text, post_image=None, post_author=current_user.user_id)
            db.session.add(user_text)
            db.session.commit()
            print(user_text, current_user.user_id)
            flash("Thanks for sharing!")
    return render_template('home.html', user=current_user)

@views.route('/feed', methods=['GET', 'POST'])
@login_required
def feed():
    if request.method == 'POST':
        postNum = request.form.get('favbtn')
        newFav = Favorites(user_id=current_user.user_id, post_id=postNum)
        exists = Favorites.query.filter_by(user_id=current_user.user_id, post_id=postNum).first()
        if exists:
            flash('This post is already a favorite!', category='error')
        else:
            db.session.add(newFav)
            db.session.commit()
    all_posts = db.session.query(Posts).all()
    def shuffle_filter(posts):
        try:
            result = list(posts)
            random.shuffle(result)
            return result
        except:
            return posts
    shuffled = shuffle_filter(all_posts)
    return render_template('feed.html', user=current_user, all_posts=shuffled)

from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
import random
from .models import Posts, Favorites
from . import db, s3, BUCKET_NAME


views = Blueprint('views', __name__)


@views.route('/')
def root_redirect():
    return redirect(url_for('auth.login'))

@views.route('/home', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST':
        text = request.form.get('post_content')
        title = request.form.get('post_title')
        post_img = request.files['p_image']
        filename = secure_filename(post_img.filename)

        if post_img:
            s3.upload_fileobj(
                Bucket = BUCKET_NAME,
                Fileobj = post_img,
                Key = filename
            )
            print('image uploaded!')

        if len(title) <1:
            flash('Please enter a title', category='error')
        if len(text) < 1:
            flash('No text entered, try again.', category='error')
        else:
            user_text = Posts(post_title=title, post_content=text, post_image=filename, post_author=current_user.user_id)
            db.session.add(user_text)
            db.session.commit()
            print(user_text, current_user.user_id)
            flash("Thanks for sharing!")
    return render_template('home.html', user=current_user)

@views.route('/feed', methods=['GET', 'POST'])
@login_required
def feed():
    if request.method == 'POST':
        see_more = request.form.get('seeMore')
        if see_more:
            return redirect(url_for('views.single_post', user=current_user, id = see_more))
        postNum = request.form.get('favbtn')
        newFav = Favorites(user_id=current_user.user_id, post_id=postNum)
        exists = Favorites.query.filter_by(user_id=current_user.user_id, post_id=postNum).first()
        if exists:
            flash('This post is already a favorite!', category='error')
        else:
            db.session.add(newFav)
            db.session.commit()
            flash('Added to favorites!', category='success')
    all_posts = db.session.query(Posts).all()
    def shuffle_posts(posts):
        try:
            result = list(posts)
            random.shuffle(result)
            return result
        except:
            return posts
    return render_template('feed.html', user=current_user, all_posts=shuffle_posts(all_posts))

@views.route('/posts', methods=['GET', 'POST'])
def single_post():
    if request.method == 'POST':
        if current_user.is_anonymous:
            flash('Please make an account or log in to add as favorite')
            postNumber = request.args.get('id')
            this_post = Posts.query.filter_by(post_id=postNumber).first()
            return render_template('single_post.html', user=current_user, post=this_post, bktname=BUCKET_NAME)
        postNum = request.form.get('favbtn')
        newFav = Favorites(user_id=current_user.user_id, post_id=postNum)
        flash('Please make an account or log in to add a favorite!', category='error')
        exists = Favorites.query.filter_by(user_id=current_user.user_id, post_id=postNum).first()
        if exists:
            flash('This post is already a favorite!', category='error')
        else:
            db.session.add(newFav)
            db.session.commit()
            flash('Added to favorites!', category='success')
    postNumber = request.args.get('id')
    this_post = Posts.query.filter_by(post_id=postNumber).first()
    return render_template('single_post.html', user=current_user, post=this_post, bktname=BUCKET_NAME)
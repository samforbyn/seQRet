from flask import Blueprint, flash, render_template, request
from flask_login import login_required, current_user
from .models import Posts
from . import db


views = Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST'])
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

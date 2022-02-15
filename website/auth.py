from flask import Blueprint, render_template, request, flash

auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    data = request.form
    print(data)
    return render_template('login.html')
@auth.route('/logout')
def logout():
    return "<p>Logout</p>"

@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == "POST":
        firstName = request.form.get('firstName')
        lastName = request.form.get('lastName')
        username = request.form.get('username')
        email = request.form.get('email')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        if len(email) < 3:
            flash('Your email needs to contain at least 3 characters, please try again.', category='error')
        elif len(firstName) < 1:
            flash('Your first name needs to contain more than 1 character, please try again.', category='error')
        elif len(lastName) < 1:
            flash('Your last name needs to contain more than 1 character, please try again.', category='error')
        elif len(username) < 4:
            flash('Your username needs to contain more than 3 character, please try again.', category='error')
        elif password1 != password2:
            flash('Passwords do not match, please try again.', category='error')
        elif len(password1) < 7:
            flash('Your password needs to contain at least 7 characters, try again.', category='error')

        else:
            flash('Account successfully created, you can log in now!')
    return render_template('sign_up.html')
from flask import Blueprint,flash, session,render_template, request, redirect, url_for
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import login_user
from ..forms import LoginForm, RegisterForm
from ..models import User

from ..extensions import db

# Create the blueprint
main = Blueprint('main', __name__)

# Home route
@main.route('/')
def index():
    return redirect('/login')

@main.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        username = form.username.data
        email = form.email.data
        password = form.password.data

        # Check if user already exists
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash('Username already exists. Try a different one.', 'danger')
            return render_template('register.html', form=form)

        # Create user
        hashed_password = generate_password_hash(password)
        new_user = User(username=username, email=email, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        login_user(new_user)

        flash('Registration successful! You are now logged in.', 'success')
        return redirect(url_for('main.home'))

    return render_template('register.html', form=form)
@main.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password, password):
            login_user(user)
            flash("Login successful!", "success")
            return redirect(url_for('main.home'))
        else:
            flash("Invalid username or password.", "danger")

    return render_template('login.html', form=form)

@main.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect('/login')
    return render_template('dashboard.html', username=session['username'])
@main.route('/logout')
def logout():
    session.clear()
    flash("Logged out!")
    return redirect('/login')
@main.route('/submit', methods=['GET', 'POST'])
def submit_bill():
    if request.method == 'POST':
        bill_text = request.form.get('bill_text')
        # Placeholder: you'll add parsing and DB logic here later
        return f"✅ Received bill: {bill_text}"
    return '''
        <form method="POST">
            <textarea name="bill_text" placeholder="Enter your bill here..."></textarea>
            <br>
            <button type="submit">Submit</button>
        </form>
    '''

@main.route('/new-bill', methods=['GET', 'POST'])
def new_bill():
    if request.method == 'POST':
      if request.method == 'POST':
        bill_text = request.form.get('bill_text')
        parsed_data = parse_bill_text(bill_text)  # You'll write this function
        print(parsed_data)  # For now, just test it
        return render_template('results.html', parsed_data=parsed_data)

    return render_template('new_bill.html')
@main.route('/bills')
def view_bills():
    return "🧾 Bills will be shown here soon!"

@main.route('/create_group', methods=['GET', 'POST'])
def create_group():
    if request.method == 'POST':
        group_name = request.form.get('group_name')
        description = request.form.get('description')
        num_participants = int(request.form.get('num_participants'))

        # Save group to DB
        new_group = Group(name=group_name, description=description)
        db.session.add(new_group)
        db.session.commit()

        # Temporarily store in session to access later
        session['group_id'] = new_group.id
        session['num_participants'] = num_participants

        return redirect(url_for('upload_routes.upload_receipt'))  # Next step

    return render_template('create_group.html')

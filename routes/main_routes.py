from flask import Blueprint,flash, session,render_template, request, redirect, url_for
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
        existing_user = User.query.filter_by(username=form.username.data).first()
        if existing_user:
            flash("Username already taken.")
            return redirect('/register')

        new_user = User(username=form.username.data, password=form.password.data)
        db.session.add(new_user)
        db.session.commit()
        flash("Registered! Please log in.")
        return redirect('/login')

    return render_template('register.html', form=form)
@main.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.password == form.password.data:
            session['user_id'] = user.id
            session['username'] = user.username
            return redirect('/dashboard')
        flash("Invalid credentials")
    return render_template('login.html', form=form)
# Bill submission route (you can extend this later)

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

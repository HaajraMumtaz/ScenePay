from flask import Blueprint,flash, session,render_template, request, redirect, url_for
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import login_user,current_user,login_required
from ..forms import LoginForm, RegisterForm, CreateGroupForm
from ..models import User, Group
from datetime import datetime

from ..extensions import db

# Create the blueprint
main = Blueprint('main', __name__)

# Home route
@main.route('/')
def home():
    return redirect('/login')

@main.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        # Check if user already exists
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash('Username already exists. Try a different one.', 'danger')
            return render_template('register.html', form=form)

        # Create user
        hashed_password = generate_password_hash(password)
        new_user = User(username=username, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        login_user(new_user)

        flash('Registration successful! You are now logged in.', 'success')
        print("ok")
        return redirect(url_for('main.dashboard'))

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
            return redirect(url_for('main.dashboard'))
        else:
            flash("Invalid username or password.", "danger")

    return render_template('login.html', form=form)

@main.route('/dashboard')
@login_required
def dashboard():
    # Query all groups created by the logged-in user
    user_groups = Group.query.filter_by(created_by=current_user.id).all()

    return render_template(
        'dashboard.html',
        username=current_user.username,
        groups=user_groups
    )

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
@login_required
def create_group():
    form = CreateGroupForm()
    if form.validate_on_submit():
        new_group = Group(
            name=form.name.data,
            created_by=current_user.id,
            created_at=datetime.utcnow(),
            description=form.description.data
        )
        db.session.add(new_group)
        db.session.commit()
        flash('Group created successfully!', 'success')
        return redirect(url_for('main.dashboard'))  # or wherever you want
    return render_template('create_group.html', form=form)


# @main.route('/groups')
# @login_required
# def groups():
#     user_groups = Group.query.filter_by(created_by=current_user.id).all()
#     return render_template('groups.html', groups=user_groups)
@main.route('/group/<int:group_id>')
@login_required
def group_detail(group_id):
    group = Group.query.get_or_404(group_id)

    # (Optional) verify user is allowed to view:
    if group.created_by != current_user.id:
        flash("You do not have permission to view this group.", "danger")
        return redirect(url_for('main.dashboard'))

    return render_template('group_detail.html', group=group)



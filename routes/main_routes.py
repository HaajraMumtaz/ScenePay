from flask import Blueprint,flash, session,render_template, request, redirect, url_for
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import login_user,current_user,login_required
from ..forms import LoginForm, RegisterForm, CreateGroupForm
from ..models import User, Group,Expense,ExpenseSplit
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

# @main.route('/new-bill', methods=['GET', 'POST'])
# def new_bill():
#     if request.method == 'POST':
#       if request.method == 'POST':
#         bill_text = request.form.get('bill_text')
#         parsed_data = parse_bill_text(bill_text)  # You'll write this function
#         print(parsed_data)  # For now, just test it
#         return render_template('results.html', parsed_data=parsed_data)

#     return render_template('new_bill.html')


@main.route('/create_group', methods=['GET', 'POST'])
@login_required
def create_group():
    form = CreateGroupForm()
    if form.validate_on_submit():
        new_group = Group(
            name=form.name.data,
            created_by=current_user.id,
            created_at=datetime.utcnow(),
            description=form.description.data,
            num_members=form.num_members.data
        )
        db.session.add(new_group)
        db.session.commit()
        flash('Group created successfully!', 'success')
 
        return redirect(url_for('upload.upload_receipt', group_id=new_group.id))
    

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

@main.route('/manual/<int:group_id>', methods=['POST', 'GET'])
@login_required
def manual_form(group_id):
    group = Group.query.get_or_404(group_id)

    if request.method == 'POST':
        data = request.form
        members = data.getlist('members')  # this doesn't work directly; we parse manually below

        for i in range(group.num_members):
            member_prefix = f"members[{i}]"
            member_name = data.get(f"{member_prefix}[name]")
            
            # ✅ Create Membership as guest
            membership = Membership(
                guest_name=member_name,
                group_id=group.id,
                is_guest=True
            )
            db.session.add(membership)
            db.session.flush()  # so we can get the membership ID

            j = 0
            while True:
                item_name = data.get(f"{member_prefix}[items][{j}][name]")
                if not item_name:
                    break  # no more items

                price = float(data.get(f"{member_prefix}[items][{j}][price]"))
                share = float(data.get(f"{member_prefix}[items][{j}][share]"))

                # ✅ Create Expense (for each item)
                expense = Expense(
                    group_id=group.id,
                    title=item_name,
                    amount=price,
                    payer_id=current_user.id  # assumed current user paid all
                )
                db.session.add(expense)
                db.session.flush()

                # ✅ Create ExpenseSplit (based on share)
                expense_split = ExpenseSplit(
                    expense_id=expense.id,
                    amount=round(price * share, 2),  # calculating share
                    user_id=None,  # unknown until guest logs in
                    status="unpaid"
                )
                db.session.add(expense_split)

                j += 1

        db.session.commit()
        flash("Manual entries recorded!", "success")
        return redirect(url_for('main.dashboard'))

    return render_template('manual_form.html', group=group)

# @main.route('/manual_form/<int:group_id>', methods=['POST'])
# @login_required
# def submit_manual_form(group_id):
#     members_data = []

#     # Get number of members from hidden input
#     num_members = int(request.form.get('num_members', 0))

#     for m in range(num_members):
#         member_name = request.form.get(f'member_{m}_name')
#         if not member_name:
#             continue

#         member_items = []
#         item_index = 0
#         while True:
#             item_name = request.form.get(f'member_{m}_item_{item_index}_name')
#             item_price = request.form.get(f'member_{m}_item_{item_index}_price')
#             item_share = request.form.get(f'member_{m}_item_{item_index}_share')

#             if not item_name:
#                 break  # No more items for this member

#             try:
#                 item_price = float(item_price)
#                 item_share = float(item_share)
#             except (ValueError, TypeError):
#                 item_price = 0
#                 item_share = 1

#             member_items.append({
#                 "name": item_name,
#                 "price": item_price,
#                 "share": item_share
#             })
#             item_index += 1

#         members_data.append({
#             "name": member_name,
#             "items": member_items
#         })

#     # (Optional) Print or log it for testing
#     print("Parsed Manual Form Data:", members_data)

#     # TODO: Save to DB or pass to template
#     flash("Form submitted successfully!", "success")
#     return redirect(url_for('main.dashboard'))

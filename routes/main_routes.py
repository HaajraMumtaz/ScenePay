from flask import Blueprint, render_template, request, redirect, url_for

# Create the blueprint
main = Blueprint('main', __name__)

# Home route
@main.route('/')
def home():
    return "👋 Welcome to BillSplitter+"

# Bill submission route (you can extend this later)
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

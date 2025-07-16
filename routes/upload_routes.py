from flask import Blueprint, render_template, request, redirect, url_for, session
from ..utils.parse import parse_bill_text
upload_bp = Blueprint('upload', __name__)

@upload_bp.route('/group/<int:group_id>/upload_receipt', methods=["GET", "POST"])
def upload_receipt(group_id):
    if request.method == "POST":
        file = request.files.get("receipt")
        if file:
            parsed_data = parse_bill_text(file) 
            session['ocr_items'] = parsed_data
        return redirect(url_for('form.form', group_id=group_id)) 

    return render_template("upload.html", group_id=group_id)
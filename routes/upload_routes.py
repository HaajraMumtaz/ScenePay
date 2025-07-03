from flask import Blueprint, render_template, request, redirect, url_for, session
upload_bp = Blueprint('upload', __name__)

@upload_bp.route("/upload", methods=["GET", "POST"])
def upload_receipt():
    if request.method == "POST":
        file = request.files.get("receipt")
        if file:
            parsed_data = extract_data_from_image(file)  # returns dict of {item: price}
            session['ocr_items'] = parsed_data
        return redirect(url_for('form.form'))  # Move to next form

    return render_template("upload.html")
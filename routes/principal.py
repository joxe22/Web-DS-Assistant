from flask import Blueprint, render_template, request, redirect, url_for
from flask import flash
import os
from werkzeug.utils import secure_filename

principal_bp = Blueprint('principal', __name__)

UPLOAD_FOLDER = 'uploads/'
ALLOWED_EXTENSIONS = {'csv'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@principal_bp.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(UPLOAD_FOLDER, filename))
            flash('File uploaded successfully')
            # Corrected line here: reference the 'data_processing.process_data' endpoint
            return redirect(url_for('data_processing.html', filename=filename))

    return render_template('index.html')

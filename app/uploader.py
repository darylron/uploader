"""UI and API for uploading images."""
import os
from flask import Blueprint, current_app, Flask, flash, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename


bp = Blueprint(
    'upload', __name__, url_prefix='/upload')


ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}


def allowed_file(file_name):
    return '.' in file_name and (
        file_name.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS)


@bp.route('/image', methods=['GET', 'POST'])
def image_file():
    if request.method == 'POST':
        # Only files with file type part will be accepted.
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']

        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
    return render_template('uploader.html')
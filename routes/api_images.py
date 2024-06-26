from flask import Blueprint, jsonify, request, redirect, url_for, render_template, current_app
import os
from werkzeug.utils import secure_filename

api_images_bp = Blueprint('api_images', __name__)

@api_images_bp.route("/")
def testing1():
    return render_template("/imagetesting.html")

@api_images_bp.route("/upload", methods = ['POST'])
def imageupload():
    if request.method == 'POST':
        f = request.files['file']
        f.save(os.path.join(current_app.config['UPLOAD_FOLDER'], secure_filename(f.filename)))
    return redirect(url_for('html.home'))
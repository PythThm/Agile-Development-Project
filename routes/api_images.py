from flask import Blueprint, jsonify, request, redirect, url_for
import os
from app import app
from werkzeug.utils import secure_filename

api_images_bp = Blueprint('api_images', __name__)

@api_images_bp.route("/upload", methods = ['POST'])
def imageupload():
    if request.method == 'POST':
        f = request.files['file']
        f.save(os.path.join(app.config['static'], secure_filename(f.filename)))
    return redirect(url_for('html.home'))
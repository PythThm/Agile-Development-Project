from flask import Blueprint, render_template

supports_bp = Blueprint("supports", __name__)

@supports_bp.route('/')
def supports():
    return render_template('supports/supports.html')

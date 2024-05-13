from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required
from models import Issue
from db import db

supports_bp = Blueprint("supports", __name__)

@supports_bp.route('/')
def supports():
    return render_template('supports/supports.html')

@supports_bp.route('/submit_issues', methods=['POST'])
@login_required
def submit_issues():
    # login code goes here
    issue_title = request.form.get('issue_title')
    issue_description = request.form.get('issue_description')

    # create a new issue
    new_issue = Issue(title=issue_title, description=issue_description)

    # add the new issue to the database
    db.session.add(new_issue)
    db.session.commit()

    flash("Issue submitted successfully!")
    return redirect(url_for('supports.issue_submitted'))


@supports_bp.route('/issue_submitted')
def issue_submitted():
    return render_template('supports/issue_submitted.html')

@supports_bp.route('/view_issues')
@login_required
def view_issues():
    issues = Issue.query.all()
    return render_template('supports/view_issues.html', issues=issues)
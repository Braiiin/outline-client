from flask import Blueprint, render_template
from flask_login import login_required

# setup Blueprint
admin = Blueprint('admin', __name__, url_prefix='/admin')


@admin.route('/')
@login_required
def home():
	"""Admin panel home"""
	return render_template('admin/home.html')


@admin.route('/outline/create')
@login_required
def create():
	"""Add a new outline"""
	return render_template('form.html')


@admin.route('/outline/<string:outlineId>/edit')
@login_required
def edit(outlineId):
	"""Edit an outline"""
	return render_template('form.html')


@admin.route('/outline/<string:outlineId>/delete')
@login_required
def delete(outlineId):
	"""Delete an outline"""
	return render_template('confirm.html')

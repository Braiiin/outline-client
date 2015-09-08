from flask import Blueprint, render_template, request, redirect, url_for, \
    jsonify
from flask_login import login_required, current_user
from outline_client.libs.outline import Outline
from client.libs.service import Service, Employment
from .forms import AddOutlineForm, EditOutlineForm
import functools

# setup admin
admin = Blueprint('admin', __name__, url_prefix='/admin')


def employee_required(f):
    """employee status required - otherwise, redirect to join page"""
    @functools.wraps(f)
    def helper(*args, **kwargs):
        service = Service(name='Outline').get_or_create()
        employee = Employment(
            user=current_user.id,
            service=service.id).fetch()
        if not employee:
            return redirect(url_for('public.join'))
        return f(*args, **kwargs)
    return helper


@admin.route('/')
@login_required
@employee_required
def home():
    """Admin panel home"""
    outlines = Outline().fetch()
    return render_template('admin/home.html', outlines=outlines)


@admin.route('/outline/create', methods=['POST', 'GET'])
@login_required
@employee_required
def outline_create():
    """Add a new outline"""
    form = AddOutlineForm(author=current_user.id)
    if request.method == 'POST':
        outline = Outline(**request.form).post()
        return redirect(url_for('admin.home'))
    return render_template('form.html', **locals())


@admin.route('/outline/<string:outlineId>/edit', methods=['POST', 'GET'])
@login_required
@employee_required
def outline_edit(outlineId):
    """Edit an outline"""
    outline = Outline(id=outlineId).get()
    outline.hashtags = ', '.join(['#'+h for h in outline.hashtags])
    form = EditOutlineForm(**outline._data)
    if request.method == 'POST':
        outline.created_at = outline.updated_at = None
        outline.load(**request.form).put()
        return redirect(url_for('admin.home'))
    return render_template('form.html', **locals())


@admin.route('/outline/<string:outlineId>/delete', methods=['POST', 'GET'])
@login_required
@employee_required
def outline_delete(outlineId):
    """Delete an outline"""
    outline = Outline(id=outlineId).get()
    if request.method == 'POST':
        outline.delete()
        return 'Successfully deleted outline "%s"' % outline.title
    return render_template('admin/confirm.html',
        cancel=url_for('admin.outline_edit', outlineId=outlineId))

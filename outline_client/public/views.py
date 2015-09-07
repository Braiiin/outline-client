from flask import jsonify, Blueprint, redirect as flask_redirect, url_for, \
    render_template, request, current_app
from flask_login import current_user, logout_user, login_user
from client.libs.core import User, Session
from client import login_manager
import functools
from outline_client.libs.outline import Outline

# setup Blueprint
public = Blueprint('public', __name__)

def redirect(location, **kwargs):
    """assembles kwargs as querystring"""
    kwargs = ['%s=%s' % pair for pair in kwargs.items()]
    location = location + '?' + '&'.join(kwargs)
    return flask_redirect(location)

# Login utilities

def anonymous_required(f):
    """Require anonymous - otherwise, redirect to private sphere"""
    @functools.wraps(f)
    def wrapper(*args, **kwargs):
        if current_user.is_authenticated():
            return redirect(url_for('admin.home'))
        return f(*args, **kwargs)
    return wrapper


@login_manager.user_loader
def load_user(access_token):
    """Loading a user from saved userId"""
    session = Session(access_token=access_token).get()
    if session:
        user = User(id=session.user, access_token=access_token).get()
        session.user = user
        if user.is_active():
            return user
    return None

@login_manager.unauthorized_handler
def unauthorized():
    """Where unauthenticated users are sent"""
    return redirect(url_for('public.login'))


@public.route('/logout')
def logout():
    """Logout the user"""
    logout_user()
    return redirect(url_for('public.login'))


# Views
@public.route('/')
def home():
    """Displays all outlines"""
    outlines = Outline().fetch()
    return render_template('public/home.html', current_user=current_user)


@public.route('/login')
@anonymous_required
def login():
    """Redirects to Braiiin core login"""
    access_token = request.args.get('access_token', None)
    if access_token:
        user = load_user(access_token)
        if user:
            login_user(user)
        return redirect(url_for('admin.home'))
    return redirect(
        '{}/login'.format(current_app.config['CORE_URI']),
        next=request.url)


@public.route('/register')
@anonymous_required
def register():
    """Redirects to Braiiin core registration"""
    access_token = request.args.get('access_token', None)
    if access_token:
        load_user(access_token)
        return redirect(url_for('admin.home'))
    return redirect(
        '{}/register'.format(current_app.config['CORE_URI']),
        next=request.url)


@public.route('/search')
def search():
    """Searches by content"""
    outlines = Outline().fetch()
    return render_template('public/search.html',
        outlines=outlines,
        current_user=current_user,
        query=request.args.get('query'))


@public.route('/outline/<string:outlineId>')
def outline(outlineId):
    """Detail view for an outline"""
    outline = Outline(id=outlineId).get()
    outline.content = outline.content.replace('\n', '<br>\n')
    return render_template('public/outline.html', outline=outline)

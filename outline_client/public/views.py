from flask import jsonify, Blueprint, redirect as flask_redirect, url_for, \
    render_template, request, current_app
from flask_login import current_user, logout_user, login_user, login_required
from client.libs.core import User, Session
from client.libs.service import Service, Employment
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
    return redirect(url_for('public.login'), next=request.url)


# Employment utilities

def nonemployee_required(f):
    """Require nonemployee - otherwise, redirect to admin"""
    @functools.wraps(f)
    def wrapper(*args, **kwargs):
        service = Service(
            name='Outline'
        ).get_or_create()
        employment = Employment(
            user=current_user.id,
            service=service.id
        ).fetch()
        if employment:
            return redirect(url_for('admin.home'))
        return f(*args, **kwargs)
    return wrapper


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
        next=request.args.get('next', request.url))


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
    outlines = Outline().search(request.args.get('query'))
    if outlines:
        outlines = [Outline(**data) for data in outlines]
    return render_template('public/search.html',
        outlines=outlines,
        current_user=current_user,
        query=request.args.get('query'))


@public.route('/outline/<string:outlineId>')
def outline(outlineId):
    """Detail view for an outline"""
    outline = Outline(id=outlineId).get().format_content()
    return render_template('public/outline.html', outline=outline)


@public.route('/join', methods=['POST', 'GET'])
@login_required
@nonemployee_required
def join():
    """join staff"""
    if request.method == 'POST':
        token = request.form.get('token', None)
        if token and token in ('wl4325hi32rf', '29sfh3mdo2sa', '2oqeo28djap2'):
            service = Service(name='Outline').get_or_create()
            employee = Employment(
                user=current_user.id,
                service=service.id).post()
            return redirect(url_for('admin.home'))
        message = 'Invalid token.'
    return render_template('public/join.html', **locals())

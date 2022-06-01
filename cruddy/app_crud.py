"""control dependencies to support CRUD app routes and APIs"""
import markdown
from flask import Blueprint, render_template, request, url_for, redirect, jsonify, make_response, session
from flask_login import login_required, current_user, login_user
from cruddy.model import coolendar, model_printerr, Discussion, Notes
from cruddy.query import *

# blueprint defaults https://flask.palletsprojects.com/en/2.0.x/api/#blueprint-objects
app_crud = Blueprint('crud', __name__,
                     url_prefix='/crud',
                     template_folder='templates/cruddy/',
                     static_folder='static',
                     static_url_path='static')

""" Blueprint is established to isolate Application control code for CRUD operations, key features:
    1.) 'Users' table control methods, controls relationship between User Actions and Database Model
    2.) Control methods are achieved using app routes for each CRUD operations
    3.) login required to restrict CRUD operations to identified users
"""


# Default URL for Blueprint
@app_crud.route('/')
def crud():
    """obtains all Users from table and loads Admin Form"""
    return render_template("crud.html", table=users_all())


@app_crud.route('/logout')
@login_required
def crud_logout():
    logout()
    return redirect(url_for('crud.crud_login'))

    return render_template("login.html")


# Unauthorised users do not get access to the SQL CRUD
# Flask-Login directs unauthorised users to this unauthorized_handler
@login_manager.unauthorized_handler
def unauthorized():
    """Redirect unauthorized users to Login page."""
    return redirect(url_for('crud.crud_login'))

# Flask-Login directs unauthorised users to this unauthorized_handler


# if login url, show phones table only
@app_crud.route('/login/', methods=["GET", "POST"])
def crud_login():
    # obtains form inputs and fulfills login requirements
    if request.form:
        email = request.form.get("email")
        password = request.form.get("password")
        if login(email, password):       # zero index [0] used as email is a tuple
            return redirect(url_for('index'))

    # if not logged in, show the login page
    return render_template("login.html")


@app_crud.route('/authorize/', methods=["GET", "POST"])
def crud_authorize():
    # check form inputs and creates user
    if request.form:
        # validation should be in HTML
        user_name = request.form.get("user_name")
        email = request.form.get("email")
        password1 = request.form.get("password1")
        password2 = request.form.get("password1")
        phone = request.form.get("phone")
        # password should be verified
        if authorize(user_name, email, password1, phone):    # zero index [0] used as user_name and email are type tuple
            return redirect(url_for('crud.crud_login'))
    # show the auth user page if the above fails for some reason
    return render_template("authorize.html")

@app_crud.route('/create/', methods=["POST"])
def create():
    """gets data from form and add it to Users table"""
    if request.form:
        po = Users(
            request.form.get("name"),
            request.form.get("email"),
            request.form.get("password"),
            request.form.get("phone")
        )
        po.create()
    return redirect(url_for('crud.crud'))
# CRUD create/add
@app_crud.route('/createCoolendar/', methods=["POST"])
def createCoolendar():
    """gets data from form and add it to Users table"""
    if request.form:
        po = coolendar(
            request.form.get("day"),
            request.form.get("information")
        )
        po.create()
    return redirect(url_for('crud.crudCalendar'))

@app_crud.route('/deleteCoolendar/', methods=["POST"])
def deleteCoolendar():
    """gets userid from form delete corresponding record from Users table"""
    if request.form:
        day = request.form.get("day")
        po = coolendar_by_day(day)
        if po is not None:
            po.delete()
    return redirect(url_for('crud.crudCalendar'))

@app_crud.route('/calendar/')
@login_required
def calendar():
        return render_template("calendar.html", table=calendar_all())






@app_crud.route('/crudcalendar/')
@login_required
def crudCalendar():
    if not current_user.email:
        return redirect(url_for('crud.crud_login'))
    admin = "admin@admin.admin"
    control = current_user.email
    if control == admin:
        return render_template("crudCalendar.html", table=calendar_all())
    else:
        return redirect(url_for('crud.crud_login'))


# CRUD read
@app_crud.route('/read/', methods=["POST"])
def read():
    """gets userid from form and obtains corresponding data from Users table"""
    table = []
    if request.form:
        userid = request.form.get("userid")
        po = user_by_id(userid)
        if po is not None:
            table = [po.read()]  # placed in list for easier/consistent use within HTML
    return render_template("crud.html", table=table)


# CRUD update
@app_crud.route('/update/', methods=["POST"])
def update():
    """gets userid and name from form and filters and then data in  Users table"""
    if request.form:
        userid = request.form.get("userid")
        name = request.form.get("name")
        po = user_by_id(userid)
        if po is not None:
            po.update(name)
    return redirect(url_for('crud.crud'))


# CRUD delete
@app_crud.route('/delete/', methods=["POST"])
def delete():
    """gets userid from form delete corresponding record from Users table"""
    if request.form:
        userid = request.form.get("userid")
        po = user_by_id(userid)
        if po is not None:
            po.delete()
    return redirect(url_for('crud.crud'))


def calendar_all():
    table = coolendar.query.all()
    json_ready = [peep.read() for peep in table]
    return json_ready


@app_crud.route('/discussioncreate/', methods=["POST"])
def discussioncreate():
    """gets data from form and add it to Users table"""
    if request.form:
        do = Discussion(
            request.form.get("posts"),
            current_user.name
        )
        do.create()
    return redirect(url_for('crud.discussion'))

@app_crud.route('/discussion/')
@login_required
def discussion():
    return render_template("discussion.html", table=discussion_all())


def discussion_all():
    table1 = Discussion.query.all()
    json_ready = [peep.read() for peep in table1]
    return json_ready

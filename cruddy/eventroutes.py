from flask import Blueprint, render_template, request, url_for, redirect
from cruddy.model import Events
from flask_login import login_required
from cruddy.query import *

app_events = Blueprint('events', __name__,
                       url_prefix='/events',
                       template_folder='templates/',
                       static_folder='static',
                       static_url_path='assets')

def events_all():
    table = Events.query.all()
    json_ready = [item.read() for item in table]
    return json_ready

def event_by_id(eventid):
    return Events.query.filter_by(eventID=eventid).first()


@app_events.route('/edit/')
@login_required
def edit():
    if not current_user.email:
        return redirect(url_for('crud.crud_login'))
    admin = "admin@admin.admin"
    control = current_user.email
    if control == admin:
        return render_template("editevents.html", table=events_all())
    else:
        return redirect(url_for('crud.crud_login'))

@app_events.route('/create/', methods=["POST"])
def create():
    if request.form:
        po=Events(
            request.form.get("name"),
            request.form.get("date"),
            request.form.get("description")
        )
        po.create()
    return render_template("editevents.html", table=events_all())

@app_events.route('/read/', methods=["POST"])
def read():
    table = []
    if request.form:
        eventid = request.form.get("eventid")
        po = event_by_id(eventid)
        if po is not None:
            table = [po.read()]
    return render_template("editevents.html", table=table)

@app_events.route('/update/', methods=["POST"])
def update():
    if request.form:
        eventid = request.form.get("eventid")
        date = request.form.get("date")
        name = request.form.get("name")
        description = request.form.get("description")
        po = event_by_id(eventid)
        if po is not None:
            po.update(date, name, description)
    return render_template("editevents.html", table=events_all())


@app_events.route('/delete/', methods=["POST"])
def delete():
    if request.form:
        eventid = request.form.get("eventid")
        po = event_by_id(eventid)
        if po is not None:
            po.delete()
    return render_template("editevents.html", table=events_all())


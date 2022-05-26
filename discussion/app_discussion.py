import markdown
from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user
from cruddy.query import user_by_id
from cruddy.model import Discussion

app_discussion = Blueprint('discussion', __name__,
                      url_prefix='/discussion',
                      template_folder='templates/discussion/',
                      static_folder='static',
                      static_url_path='static')

@app_discussion.route('/discussion')
@login_required
def discussion():
    table = []
    if request.form:
        userid = request.form.get("uid")
        po = user_by_id(userid)
        if po is not None:
            table = [po.read()]  # placed in list for easier/consistent use within HTML
    return render_template("discussion.html", table=table)

@app_discussion.route('/create/', methods=["POST"])
def create():
    """gets data from form and add it to Users table"""
    if request.form:
        po = Discussion(
            request.form.get("post")
        )
        po.create()
    return redirect(url_for('discussion.discussion'))
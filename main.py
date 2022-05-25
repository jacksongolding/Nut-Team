# import "packages" from flask
from flask import request, render_template

from __init__ import app
from cruddy.app_crud import app_crud
from cruddy.app_crud_api import app_crud_api

app.register_blueprint(app_crud)
app.register_blueprint(app_crud_api)

# create a Flask instance



# connects default URL to render index.html
@app.route('/')
def index():
    return render_template("index.html")

@app.route('/quiz/')
def quiz():
    return render_template("quiz.html")

@app.route('/Results/')
def Results():
    return render_template("Results.html")

@app.route('/Squid/')
def Squid():
    return render_template("Squid.html")

@app.route('/Building/')
def Building():
    return render_template("Building.html")

@app.route('/calendar/')
def calendar():
    return render_template("calendar.html")

@app.route('/overview/')
def overview():
    return render_template("overview.html")

@app.route('/study/')
def study():
    return render_template("study.html")

@app.route('/test/')
def test():
    return render_template("test.html")

@app.route('/importantevents/')
def importantevents():
    return render_template("importantevents.html")



@app.route('/LUCAS', methods=['GET', 'POST'])
def LUCAS():
    # submit button has been pushed
    if request.form:
        name = request.form.get("name")
        if len(name) != 0:  # input field has content
            return render_template("Lucas.html", name=name)
    # starting and empty input default
    return render_template("Lucas.html", name="World")


@app.route('/RITHWIKH', methods=['GET', 'POST'])
def RITHWIKH():
    # submit button has been pushed
    if request.form:
        name = request.form.get("name")
        if len(name) != 0:  # input field has content
            return render_template("Rithwikh.html", name=name)
    # starting and empty input default
    return render_template("Rithwikh.html", name="World")


# runs the application on the development server
if __name__ == "__main__":
    app.run(debug=True)


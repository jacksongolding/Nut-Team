# import "packages" from flask
from flask import Flask, request, render_template
import requests
import json

# create a Flask instance
app = Flask(__name__)


# connects default URL to render index.html
@app.route('/')
def index():
    return render_template("index.html")


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

@app.route('/Lorde/')
def Lorde():
    return render_template("Lorde.html")

@app.route('/Gennalyn/')
def Gennalyn():
    return render_template("Gennalyn.html")

@app.route('/JustinBieber/')
def JustinBieber():
    return render_template("JustinBieber.html")

@app.route('/OliviaRodrigo/')
def OliviaRodrigo():
    return render_template("OliviaRodrigo.html")

@app.route('/Stray/')
def Stray():
    return render_template("Stray.html")

@app.route('/Jonas/')
def Jonas():
    return render_template("Jonas.html")

@app.route('/Movie/')
def movie():
    return render_template("Movie.html")

@app.route('/Weeknd/')
def Weeknd():
    return render_template("Weeknd.html")

@app.route('/BrunoMars/')
def BrunoMars():
    return render_template("BrunoMars.html")

@app.route('/LilNasX/')
def LilNasX():
    return render_template("lilNasX.html")

@app.route('/BTS/')
def BTS():
    return render_template("BTS.html")


@app.route('/DojaCat/')
def DojaCat():
    return render_template("DojaCat.html")





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


@app.route('/ALI', methods=['GET', 'POST'])
def ALI():
    # submit button has been pushed
    if request.form:
        name = request.form.get("name")
        if len(name) != 0:  # input field has content
            return render_template("Ali.html", name=name)
    # starting and empty input default
    return render_template("Ali.html", name="World")





# runs the application on the development server
if __name__ == "__main__":
    app.run(debug=True)


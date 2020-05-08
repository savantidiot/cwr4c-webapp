from flask import render_template, url_for
from webapp import app
from webapp.models import Cancer, Intervention

@app.route("/")
@app.route("/home")
def home():
    cancers = Cancer.query.all()
    drugs = Intervention.query.all()
    return render_template('home.html', cancers=cancers, drugs=drugs)

@app.route("/about")
def about():
    return render_template('study_list.html')

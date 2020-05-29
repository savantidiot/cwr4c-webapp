from flask import render_template, url_for, request
from webapp import app, db
from webapp.models import Cancer, Intervention, Association, Article, Rank
import json
from sqlalchemy.sql import func

# The web site routes
@app.route("/", methods=['GET', 'POST'])
@app.route("/home", methods=['GET','POST'])
def home():
    cancers = Cancer.query.all()
    drugs = Intervention.query.all()
    ranks = Rank.query.order_by(Rank.rank.desc()).all()
    filter_cancers = []
    filter_drugs = []

    # Accepts post requests to update the page based on cancer and drug types
    # selected by user
    if request.method == "POST":
        filter_cancers = json.loads(request.form['cancers'])
        filter_drugs = json.loads(request.form['drugs'])

        ranks = db.session.query(Rank).filter(
            func.lower(Rank.cancer).in_(filter_cancers), func.lower(Rank.intervention).in_(filter_drugs)
        ).order_by(
            Rank.rank.desc()
        ).all()

    return render_template('home.html', cancers=cancers, drugs=drugs, ranks=ranks)

# Filler about page, currently leads to page with all studies listed
@app.route("/about")
def about():
    #pagination object
    page=request.args.get('page', 1, type=int)
    articles = Article.query.paginate(page=page, per_page=10)
    return render_template('study_list.html', articles=articles)

# Results page url changes depending on what filters are passed in
@app.route("/results/")
def results():

    page=request.args.get('page', 1, type=int)

    #cancer and drug type are always present but association could be all associations
    cancer = request.args.get('cancer', default = '*')
    intervention = request.args.get('intervention', default = '*')
    association = request.args.get('association', default = '*')
    query = db.session.query(Article)
    if cancer != '*':
        query = query.filter_by(cancer=cancer)
    if intervention != '*':
        query = query.filter_by(intervention=intervention)
    # filter by association currently not working
    if association != '*':
        articles = query.filter(func.lower(Article.association)==func.lower(association))

    #pagination object
    query =  query.paginate(page=page, per_page=10)

    return render_template('study_list.html', articles=query)

# url for article page based on pmid
@app.route("/article/<int:pmid>")
def article(pmid):
    article = Article.query.filter_by(pmid = pmid).first_or_404()
    return render_template('article.html', article=article)

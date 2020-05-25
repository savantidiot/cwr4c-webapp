from flask import render_template, url_for, request
from webapp import app, db
from webapp.models import Cancer, Intervention, Association, Article, Rank
import json

@app.route("/", methods=['GET', 'POST'])
@app.route("/home", methods=['GET','POST'])
def home():
    cancers = Cancer.query.all()
    drugs = Intervention.query.all()
    ranks = Rank.query.order_by(Rank.rank.desc()).all()
    filter_cancers = []
    filter_drugs = []

    if request.method == "POST":
        filter_cancers = json.loads(request.form['cancers'])
        filter_drugs = json.loads(request.form['drugs'])

        ranks = db.session.query(Rank).filter(
            func.lower(Rank.cancer).in_(filter_cancers), func.lower(Rank.intervention).in_(filter_drugs)
        ).order_by(
            Rank.rank.desc()
        ).all()

    return render_template('home.html', cancers=cancers, drugs=drugs, ranks=ranks)

@app.route("/about")
def about():
    #pagination object
    page=request.args.get('page', 1, type=int)
    articles = Article.query.paginate(page=page, per_page=10)
    return render_template('study_list.html', articles=articles)

@app.route("/results/")
def results():
    #pagination object
    page=request.args.get('page', 1, type=int)

    #cancer and drug type are always present but association could be all
    cancer = request.args.get('cancer', default = '*')
    intervention = request.args.get('intervention', default = '*')
    association = request.args.get('association', default = '*')
    query = db.session.query(Article)
    if cancer != '*':
        query = query.filter_by(cancer=cancer)
    if intervention != '*':
        query = query.filter_by(intervention=intervention)
    if association != '*':
        articles = query.filter_by(association=association)

    query =  query.paginate(page=page, per_page=10)

    return render_template('study_list.html', articles=query)

@app.route("/article/<int:article_id>")
def article(article_id):
    article = Article.query.get_or_404(article_id)
    return render_template('article.html', article=article)

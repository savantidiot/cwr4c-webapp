from webapp import db
import pandas as pd
from sqlalchemy.sql import func

class Cancer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cancer_type = db.Column(db.String(100), unique=True, nullable=False)

    #cancer_id =
    def __repr__(self):
        return f"Cancer Type('{self.cancer_type}')"

class Intervention(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    intervention_type = db.Column(db.String(100), unique=True, nullable=False)

    def __repr__(self):
        return f"Drug Type('{self.intervention_type}')"
#
# class Outcome(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     outcome_name = db.Column(db.String(100), unique=True, nullable=False)
#
class Association(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    association = db.Column(db.String(40), unique=True, nullable=False)
    def __repr__(self):
        return f"Association('{self.association}')"

class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    pmid = db.Column(db.Integer, nullable=False, unique=True)
    title = db.Column(db.String(500))
    abstract = db.Column(db.String(8,000))
    study_type = db.Column(db.String(100))
    cancer = db.Column(db.String(100)) # db.ForeignKey('cancer.id')
    intervention = db.Column(db.String(100)) #db.ForeignKey('intervention.id')
    association = db.Column(db.String(40)) # association = db.Column(db.Integer db.ForeignKey('association.id'))\
    def __repr__(self):
        return f"Article('{self.pmid}', '{self.title}',  '{self.cancer}', '{self.intervention}')"

class Rank(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cancer = db.Column(db.String(100))
    intervention = db.Column(db.String(100))
    effective = db.Column(db.Integer, nullable=False, default=0)
    inconclusive = db.Column(db.Integer, nullable=False, default=0)
    detrimental = db.Column(db.Integer, nullable=False, default=0)
    all = db.Column(db.Integer, nullable=False, default=0)
    rank = db.Column(db.Float, nullable=False, default=0)

    def __init__(self, **kwargs):
        super(Rank, self).__init__(**kwargs)
        self.rank = self.effective - self.detrimental;

    def __repr__(self):
        return f"Rank('{self.intervention}', '{self.cancer}')"

#  Scoring table separate table for cancer,drug, and counts

db.create_all()

c_df = pd.read_csv("webapp/cancers.csv", header=None)
#import pdb; pdb.set_trace()
cancers = c_df[0].values
for c in cancers:
    not_exists = db.session.query(
    Cancer.cancer_type
    ).filter(func.lower(Cancer.cancer_type)==func.lower(c)).scalar() is None
    if not_exists:
        new_c = Cancer(cancer_type=c)
        db.session.add(new_c)

d_df = pd.read_csv("webapp/drugs.csv", header=None)
#import pdb; pdb.set_trace()
drugs = d_df[0].values
for d in drugs:
    not_exists = db.session.query(
    Intervention.intervention_type
    ).filter(func.lower(Intervention.intervention_type)==func.lower(d)).scalar() is None
    if not_exists:
        new_d = Intervention(intervention_type=d)
        db.session.add(new_d)

article_df = pd.read_csv("webapp/articles.csv", header=0)
for index, row in article_df.iterrows():
    # check if entry with same pmid, drug, and cancer is present
    # c_id = db.session.query(
    # Cancer.id
    # ).filter_by(cancer_type=row.disease)
    #
    # d_id = db_session.query(
    #     Intervention.id
    # ).filter_by(intervention_type=row.drugs)

    #if (c_id is not None and d_id is not None):
    not_exists = db.session.query(Article).filter_by(pmid=row.pmid,
    cancer=row.disease, intervention=row.drugs).scalar() is None

    if not_exists:
        #import pdb; pdb.set_trace()
        new_a = Article(pmid=row.pmid, title=row.title, abstract=row.abstract,
        study_type=row['study type'], cancer=row.disease, intervention=row.drugs,
        association=row.association)


        db.session.add(new_a)

# populate the rank table
# currently no article matches so all 0
for c in db.session.query(func.lower(Article.cancer)).distinct():
    for d in db.session.query(func.lower(Article.intervention)).distinct():
        #import pdb; pdb.set_trace()
        all = Article.query.filter(Article.cancer.ilike(c[0])).filter(Article.intervention.ilike(d[0]))
        effective = all.filter(Article.association.ilike("Effective")).count();
        detrimental = all.filter(Article.association.ilike("Detrimental")).count();
        inconclusive = all.filter(Article.association.ilike("No effect")).count();

        not_exists = db.session.query(Rank).filter(
                func.lower(Rank.cancer)==func.lower(c[0]), func.lower(Rank.intervention)==func.lower(d[0])
            ).scalar() is None
        if not_exists:
            new_rank = Rank(
            all=all.count(),
            cancer=c[0],
            intervention=d[0],
            effective=effective,
            inconclusive=inconclusive,
            detrimental=detrimental
            )
            db.session.add(new_rank)

db.session.commit();

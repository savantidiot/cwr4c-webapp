from webapp import db
import pandas as pd

class Cancer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cancer_type = db.Column(db.String(100), unique=True, nullable=False)
    cancer_id =
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
    association_id = db.Column(db.Integer, db.ForeignKey('association.id'))

    def __repr__(self):
        return f"Article('{self.pmid}', '{self.title}')"

#
# class Article_Has_Association(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     article_id = db.Column(db.Integer, db.ForeignKey('article.id'))
#     cancer_id = db.Column(db.Integer, db.ForeignKey('cancer.id'))
#     intervention_id = db.Column(db.Integer, db.ForeignKey('intervention.id'))
#     therapeutic_association_id = db.Column(db.Integer, db.ForeignKey('therapeutic_association.id')

db.create_all()

c_df = pd.read_csv("webapp/cancers.csv", header=None)
#import pdb; pdb.set_trace()
cancers = c_df[0].values
for c in cancers:
    not_exists = db.session.query(
    Cancer.cancer_type
    ).filter_by(cancer_type=c).scalar() is None
    if not_exists:
        new_c = Cancer(cancer_type=c)
        db.session.add(new_c)

d_df = pd.read_csv("webapp/drugs.csv", header=None)
#import pdb; pdb.set_trace()
drugs = d_df[0].values
for d in drugs:
    not_exists = db.session.query(
    Intervention.intervention_type
    ).filter_by(intervention_type=d).scalar() is None
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

    assoc_id = db.session.query(
        Association.id
    ).filter_by(association=row.association)

    #if (c_id is not None and d_id is not None):
    not_exists = db.session.query(Article).filter_by(pmid=row.pmid,
    cancer=row.disease, intervention=row.drugs).scalar() is None

    if not_exists:
        #import pdb; pdb.set_trace()
        new_a = Article(pmid=row.pmid, title=row.title, abstract=row.abstract,
        study_type=row['study type'], cancer=row.disease, intervention=row.drugs,
        association_id=assoc_id)

        db.session.add(new_a)


db.session.commit();

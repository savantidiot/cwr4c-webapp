from webapp import db
from webapp.models import Article

class Studies:
    def update_studies(self, cancer, drug):.all()
        article_ids = db.session.query(Article_Has_Association.article_id)
        .filter_by(cancer_id=cancer and intervention_id=drug)
        articles = db.session.query(Article).filter_by(id.in_(article_ids00))
        return render_template('study_list.html', studies=articles)

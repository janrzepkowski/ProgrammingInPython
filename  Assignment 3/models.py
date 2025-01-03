from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class DataPoint(db.Model):
    __tablename__ = 'data_points'
    id = db.Column(db.Integer, primary_key=True)
    feature1 = db.Column(db.Float, nullable=False)
    feature2 = db.Column(db.Float, nullable=False)
    category = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"<DataPoint id={self.id} feature1={self.feature1} feature2={self.feature2} category={self.category}>"

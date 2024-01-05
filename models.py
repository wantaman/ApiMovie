from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Movie(db.Model):
    __tablename__ = 'show'
    
    show_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    running_time = db.Column(db.Integer, nullable=False)
    language = db.Column(db.String(100), nullable=False)
    genre = db.Column(db.String(100), nullable=False)
    release_date = db.Column(db.DateTime, nullable=False),
    cast_detail = db.Column(db.String(255), nullable=False)
    

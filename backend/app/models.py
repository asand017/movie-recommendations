from sqlalchemy.orm import Mapped, mapped_column
from app import db

class Movie(db.Model):
    __tablename__ = "movies"
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(db.String(255), nullable=False)
    genre: Mapped[str] = mapped_column(db.String(255))
    year: Mapped[int]
    description: Mapped[str] = mapped_column(db.Text)

class User(db.Model):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(db.String(255), unique=True, nullable=False)
    email: Mapped[str] = mapped_column(db.String(255), unique=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(db.String(255), nullable=False)

class Rating(db.Model):
    __tablename__ = "ratings"
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    movie_id: Mapped[int] = mapped_column(db.Integer, db.ForeignKey('movies.id'), nullable=False)
    rating: Mapped[float] = mapped_column(db.Float, nullable=False)
    review: Mapped[str] = mapped_column(db.Text)

    # define foreign keys
    user = db.relationship('User', backref=db.backref('ratings', lazy=True))
    movie = db.relationship('Movie', backref=db.backref('ratings', lazy=True))

class Recommendation(db.Model):
    __tablename__ = 'recommendations'
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    movie_id: Mapped[int] = mapped_column(db.Integer, db.ForeignKey('movies.id'), nullable=False)

    # define foreign keys
    user = db.relationship('User', backref=db.backref('recommendations', lazy=True))
    movie = db.relationship('Movie', backref=db.backref('recommendations', lazy=True))



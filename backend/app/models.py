from sqlalchemy.orm import Mapped, mapped_column
from app import db

class Movie(db.Model):
    __tablename__ = "movies"
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(db.String(255), nullable=False)
    genre: Mapped[str] = mapped_column(db.String(255))
    year: Mapped[int]
    directors: Mapped[str] = mapped_column(db.String(255), nullable=False)
    runtime: Mapped[int]
    description: Mapped[str] = mapped_column(db.Text, nullable=True)
    review: Mapped[str] = mapped_column(db.Text, nullable=True)
    imdb_rating: Mapped[float] = mapped_column(db.Float)
    imdb_votes: Mapped[int]
    imdb_id: Mapped[str] = mapped_column(db.String(50), nullable=False)
    
    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'genre': self.genre,
            'year': self.year,
            'directors': self.directors,
            'runtime': self.runtime,
            'description': self.description,
            'review': self.review,
            'imdb_rating': self.imdb_rating,
            'imdb_votes': self.imdb_votes,
            'imdb_id': self.imdb_id
        }

class User(db.Model):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(db.String(255), unique=True, nullable=False)
    email: Mapped[str] = mapped_column(db.String(255), unique=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(db.String(255), nullable=False)

# TODO: use migration pattern for db changes, want to add critics and audience ratings tables for rottentomatoes data
class Rating(db.Model):
    __tablename__ = "ratings"
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    movie_id: Mapped[int] = mapped_column(db.Integer, db.ForeignKey('movies.id'), nullable=False)
    rating: Mapped[float] = mapped_column(db.Float, nullable=False)
    count: Mapped[int]
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



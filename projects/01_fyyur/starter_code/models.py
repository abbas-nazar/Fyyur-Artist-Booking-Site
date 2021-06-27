from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class StateCity(db.Model):
    __tablename__ = 'StateCity'

    id = db.Column(db.Integer, primary_key=True)
    city = db.Column(db.String(120))
    venues = db.relationship("Venue", back_populates="state_city")
    artists = db.relationship("Artist", back_populates="state_city")


genre_venue_association_table = db.Table('genre_venues',
    db.Column('genre_id', db.Integer, db.ForeignKey('Genre.id')),
    db.Column('venue_id', db.Integer, db.ForeignKey('Venue.id'))
)

genre_artist_association_table = db.Table('genre_artists',
    db.Column('genre_id', db.Integer, db.ForeignKey('Genre.id')),
    db.Column('artist_id', db.Integer, db.ForeignKey('Artist.id'))
)

class Genre(db.Model):
    __tablename__ = 'Genre'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))
    venues = db.relationship("Venue", secondary=genre_venue_association_table, back_populates="genres")
    artists = db.relationship("Venue", secondary=genre_artist_association_table, back_populates="genres")

class Venue(db.Model):
    __tablename__ = 'Venue'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    address = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    statecity_id = db.Column(db.Integer, db.ForeignKey('StateCity.id'))
    shows = db.relationship("Show", back_populates="venue")

class Artist(db.Model):
    __tablename__ = 'Artist'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    phone = db.Column(db.String(120))
    genres = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    statecity_id = db.Column(db.Integer, db.ForeignKey('StateCity.id'))
    shows = db.relationship("Show", back_populates="artist")


class Show(db.Model):
    __tablename__ = 'Show'

    id = db.Column(db.Integer, primary_key=True)
    start_time = db.Column(db.DateTime, nullable=False)
    artist_id = db.Column(db.Integer, db.ForeignKey('Artist.id'))
    venue_id = db.Column(db.Integer, db.ForeignKey('Venue.id'))

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class StateCity(db.Model):
    __tablename__ = 'StateCity'

    id = db.Column(db.Integer, primary_key=True)
    state = db.Column(db.String(120))
    city = db.Column(db.String(120))
    venues = db.relationship("Venue", backref=db.backref('venue_state_city', lazy=True))
    artists = db.relationship("Artist", backref=db.backref('artist_state_city', lazy=True))

class Venue(db.Model):
    __tablename__ = 'Venue'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    address = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    genres = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    website = db.Column(db.String(120))
    seeking_talent = db.Column(db.Boolean)
    seeking_description = db.Column(db.String(500))
    statecity_id = db.Column(db.Integer, db.ForeignKey('StateCity.id'))
    state_city = db.relationship("StateCity")
    shows = db.relationship("Show", backref=db.backref('show_venue', lazy=True))


class Artist(db.Model):
    __tablename__ = 'Artist'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    phone = db.Column(db.String(120))
    genres = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    seeking_venue = db.Column(db.Boolean)
    seeking_description = db.Column(db.String(500))
    statecity_id = db.Column(db.Integer, db.ForeignKey('StateCity.id'))
    state_city = db.relationship("StateCity")
    shows = db.relationship("Show", backref=db.backref('show_artist', lazy=True))


class Show(db.Model):
    __tablename__ = 'Show'

    id = db.Column(db.Integer, primary_key=True)
    start_time = db.Column(db.DateTime, nullable=False)
    artist_id = db.Column(db.Integer, db.ForeignKey('Artist.id'))
    venue_id = db.Column(db.Integer, db.ForeignKey('Venue.id'))

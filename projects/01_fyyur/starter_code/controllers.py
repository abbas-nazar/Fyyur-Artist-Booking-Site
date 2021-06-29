from datetime import datetime

from flask import Blueprint, render_template, request, flash, redirect, url_for
from forms import ArtistForm, ShowForm, VenueForm

from models import Artist, Show, Venue, StateCity, db

controllers = Blueprint('', __name__)
@controllers.route('/')
def index():
  return render_template('pages/home.html')


#  Venues
#  ----------------------------------------------------------------

@controllers.route('/venues')
def venues():
  shows_data = []
  state_cities = StateCity.query.all()
  for state_city in state_cities:
    state_city_data = {
      "city": state_city.city,
      "state": state_city.state,
    }
    venues = []
    for venue in state_city.venues:
      venue_data = {
        'id': venue.id,
        'name': venue.name,
        'num_upcoming_shows': db.session.query(db.func.count(Show.id).label('total')).filter(
          Show.venue_id==venue.id, Show.start_time > datetime.now()).first()[0]
      }

      venues.append(venue_data)
    state_city_data['venues'] = venues
    shows_data.append(state_city_data)
  return render_template('pages/venues.html', areas=shows_data)

@controllers.route('/venues/search', methods=['POST'])
def search_venues():
  search_term = request.form.get('search_term', '')
  search = "%{}%".format(search_term)
  venues_data = []
  for venue in Venue.query.filter(Venue.name.ilike(search)).all():
    venues_data.append({
      "id": venue.id,
      "name": venue.name,
      "num_upcoming_shows": db.session.query(db.func.count(Show.id).label('total')).filter(
          Show.venue_id==venue.id, Show.start_time > datetime.now()).first()[0],
    })
  response={
    "count": len(venues_data),
    "data": venues_data
  }
  return render_template('pages/search_venues.html', results=response, search_term=search_term)

@controllers.route('/venues/<int:venue_id>')
def show_venue(venue_id):
  venue = Venue.query.get(venue_id)
  venue_data = {
    "id": venue.id,
    "name": venue.name,
    "genres": [venue.genres],
    "address": venue.address,
    "city": venue.state_city.city,
    "state": venue.state_city.state,
    "phone": venue.phone,
    "website": venue.website,
    "facebook_link": venue.facebook_link,
    "seeking_talent": venue.seeking_talent,
    "seeking_description": venue.seeking_description,
    "image_link": venue.image_link,
    "past_shows": [{
      "artist_id": 4,
      "artist_name": "Guns N Petals",
      "artist_image_link": "https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80",
      "start_time": "2019-05-21T21:30:00.000Z"
    }],
    "upcoming_shows": [{
      "venue_id": show.venue_id,
      "venue_name": show.show_venue.name,
      "artist_id": show.artist_id,
      "artist_name": show.show_artist.name,
      "artist_image_link": show.show_artist.image_link,
      "start_time": show.start_time.strftime("%Y-%m-%dT%H:%M:%S")
    } for show in Show.query.filter(Show.venue_id == venue_id, Show.start_time > datetime.now()).all()],
    "past_shows_count": db.session.query(db.func.count(Show.id).label('total')).filter(
          Show.venue_id == venue.id, Show.start_time <= datetime.now()).first()[0],
    "upcoming_shows_count": db.session.query(db.func.count(Show.id).label('total')).filter(
          Show.venue_id == venue.id, Show.start_time > datetime.now()).first()[0],
  }
  return render_template('pages/show_venue.html', venue=venue_data)

#  Create Venue
#  ----------------------------------------------------------------

@controllers.route('/venues/create', methods=['GET'])
def create_venue_form():
  form = VenueForm()
  return render_template('forms/new_venue.html', form=form)

@controllers.route('/venues/create', methods=['POST'])
def create_venue_submission():
  try:
    state = request.form.get('state')
    city = request.form.get('city')
    state_city = StateCity.query.filter(StateCity.state == state, StateCity.city == city).first()
    if not state_city:
      state_city = StateCity(state=state, city=city)
      db.session.add(state_city)
    name = request.form.get('name')
    address = request.form.get('address')
    phone = request.form.get('phone')
    genres = request.form.get('genres')
    image_link = request.form.get('image_link')
    facebook_link = request.form.get('facebook_link')
    website = request.form.get('website_link')
    seeking_talent = True if request.form.get('seeking_talent') == 'y' else False
    seeking_description = request.form.get('seeking_description')
    venue = Venue(name=name, address=address, phone=phone, genres=genres, image_link=image_link,
                  facebook_link=facebook_link, seeking_talent=seeking_talent, seeking_description=seeking_description,
                  website=website)
    venue.state_city = state_city
    db.session.add(venue)
    db.session.commit()
    flash('Venue ' + request.form['name'] + ' was successfully listed!')
  except:
    flash('An error occurred. Venue ' + name + ' could not be listed.')
  finally:
    db.session.close()
  return render_template('pages/home.html')

@controllers.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
  # TODO: Complete this endpoint for taking a venue_id, and using
  # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.

  # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that
  # clicking that button delete it from the db then redirect the user to the homepage
  return None

#  Artists
#  ----------------------------------------------------------------
@controllers.route('/artists')
def artists():
  artists = Artist.query.all()
  return render_template('pages/artists.html', artists=artists)

@controllers.route('/artists/search', methods=['POST'])
def search_artists():
  search_term = request.form.get('search_term', '')
  search = "%{}%".format(search_term)
  artists_data = []
  for artist in Artist.query.filter(Artist.name.ilike(search)).all():
    artists_data.append({
      "id": artist.id,
      "name": artist.name,
      "num_upcoming_shows": db.session.query(db.func.count(Show.id).label('total')).filter(
        Show.artist_id == artist.id, Show.start_time > datetime.now()).first()[0],
    })
  response = {
    "count": len(artists_data),
    "data": artists_data
  }
  return render_template('pages/search_artists.html', results=response, search_term=request.form.get('search_term', ''))

@controllers.route('/artists/<int:artist_id>')
def show_artist(artist_id):
  artist = Artist.query.get(artist_id)
  artist_data = {
    "id": artist.id,
    "name": artist.name,
    "genres": [artist.genres],
    "city": artist.state_city.city,
    "state": artist.state_city.state,
    "phone": artist.phone,
    "facebook_link": artist.facebook_link,
    "seeking_venue": artist.seeking_venue,
    "image_link": artist.image_link,
    "seeking_description": artist.seeking_description,
    "past_shows": [{
      "venue_id": show.venue_id,
      "venue_name": show.show_venue.name,
      "artist_id": show.artist_id,
      "artist_name": show.show_artist.name,
      "artist_image_link": show.show_artist.image_link,
      "start_time": show.start_time.strftime("%Y-%m-%dT%H:%M:%S")
    } for show in Show.query.filter(Show.artist_id == artist_id, Show.start_time <= datetime.now()).all()],
    "upcoming_shows": [{
      "venue_id": show.venue_id,
      "venue_name": show.show_venue.name,
      "artist_id": show.artist_id,
      "artist_name": show.show_artist.name,
      "artist_image_link": show.show_artist.image_link,
      "start_time": show.start_time.strftime("%Y-%m-%dT%H:%M:%S")
    } for show in Show.query.filter(Show.artist_id == artist_id, Show.start_time > datetime.now()).all()],
    "past_shows_count": db.session.query(db.func.count(Show.id).label('total')).filter(
      Show.artist_id == artist_id, Show.start_time <= datetime.now()).first()[0],
    "upcoming_shows_count": db.session.query(db.func.count(Show.id).label('total')).filter(
      Show.artist_id == artist_id, Show.start_time > datetime.now()).first()[0],
  }
  return render_template('pages/show_artist.html', artist=artist_data)

#  Update
#  ----------------------------------------------------------------
@controllers.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
  form = ArtistForm()
  artist={
    "id": 4,
    "name": "Guns N Petals",
    "genres": ["Rock n Roll"],
    "city": "San Francisco",
    "state": "CA",
    "phone": "326-123-5000",
    "website": "https://www.gunsnpetalsband.com",
    "facebook_link": "https://www.facebook.com/GunsNPetals",
    "seeking_venue": True,
    "seeking_description": "Looking for shows to perform at in the San Francisco Bay Area!",
    "image_link": "https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80"
  }
  # TODO: populate form with fields from artist with ID <artist_id>
  return render_template('forms/edit_artist.html', form=form, artist=artist)

@controllers.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
  # TODO: take values from the form submitted, and update existing
  # artist record with ID <artist_id> using the new attributes

  return redirect(url_for('show_artist', artist_id=artist_id))

@controllers.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
  form = VenueForm()
  venue={
    "id": 1,
    "name": "The Musical Hop",
    "genres": ["Jazz", "Reggae", "Swing", "Classical", "Folk"],
    "address": "1015 Folsom Street",
    "city": "San Francisco",
    "state": "CA",
    "phone": "123-123-1234",
    "website": "https://www.themusicalhop.com",
    "facebook_link": "https://www.facebook.com/TheMusicalHop",
    "seeking_talent": True,
    "seeking_description": "We are on the lookout for a local artist to play every two weeks. Please call us.",
    "image_link": "https://images.unsplash.com/photo-1543900694-133f37abaaa5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=400&q=60"
  }
  # TODO: populate form with values from venue with ID <venue_id>
  return render_template('forms/edit_venue.html', form=form, venue=venue)

@controllers.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
  # TODO: take values from the form submitted, and update existing
  # venue record with ID <venue_id> using the new attributes
  return redirect(url_for('show_venue', venue_id=venue_id))

#  Create Artist
#  ----------------------------------------------------------------

@controllers.route('/artists/create', methods=['GET'])
def create_artist_form():
  form = ArtistForm()
  return render_template('forms/new_artist.html', form=form)

@controllers.route('/artists/create', methods=['POST'])
def create_artist_submission():
  try:
    state = request.form.get('state')
    city = request.form.get('city')
    state_city = StateCity.query.filter(StateCity.state == state, StateCity.city == city).first()
    if not state_city:
      state_city = StateCity(state=state, city=city)
      db.session.add(state_city)
    name = request.form.get('name')
    phone = request.form.get('phone')
    genres = request.form.get('genres')
    image_link = request.form.get('image_link')
    facebook_link = request.form.get('facebook_link')
    seeking_description = request.form.get('seeking_description')
    seeking_venue = True if request.form.get('seeking_venue') == 'y' else False
    artist = Artist(name=name, phone=phone, image_link=image_link, facebook_link=facebook_link,
                    seeking_venue=seeking_venue, genres=genres, seeking_description=seeking_description)
    artist.state_city = state_city
    db.session.add(artist)
    db.session.commit()
    flash('Artist ' + request.form['name'] + ' was successfully listed!')
  except:
    flash('An error occurred. Artist ' + name + ' could not be listed.')
  finally:
    db.session.close()
  return render_template('pages/home.html')


#  Shows
#  ----------------------------------------------------------------

@controllers.route('/shows')
def shows():
  data = []
  for show in Show.query.all():
    show_data = {
      "venue_id": show.venue_id,
      "venue_name": show.show_venue.name,
      "artist_id": show.artist_id,
      "artist_name": show.show_artist.name,
      "artist_image_link": show.show_artist.image_link,
      "start_time": show.start_time.strftime("%Y-%m-%dT%H:%M:%S"),
      "num_upcoming_shows": db.session.query(db.func.count(Show.id).label('total')).filter(
          Show.venue_id==show.venue_id, Show.start_time > datetime.now()).first()[0],
    }
    data.append(show_data)
  return render_template('pages/shows.html', shows=data)

@controllers.route('/shows/create')
def create_shows():
  # renders form. do not touch.
  form = ShowForm()
  return render_template('forms/new_show.html', form=form)

@controllers.route('/shows/create', methods=['POST'])
def create_show_submission():
  try:
    artist_id = request.form.get('artist_id')
    venue_id = request.form.get('venue_id')
    start_time = request.form.get('start_time')
    show = Show(artist_id=artist_id, venue_id=venue_id, start_time=start_time)
    db.session.add(show)
    db.session.commit()
    flash('Show was successfully listed!')
  except:
    flash('An error occurred. Show could not be listed.')
  finally:
    db.session.close()
  return render_template('pages/home.html')

@controllers.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

@controllers.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500
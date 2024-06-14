from flask import Flask, request, jsonify, render_template
from models import db, Artist, Album, Song
from config import Config

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

# Home page route
@app.route('/')
def index():
    return render_template('index.html')

# Artists routes
@app.route('/artists', methods=['POST', 'GET'])
def artists():
    if request.method == 'POST':
        data = request.form
        new_artist = Artist(name=data['name'])
        db.session.add(new_artist)
        db.session.commit()
        # return jsonify({'id': new_artist.id, 'name': new_artist.name}), 201
    # elif request.method == 'GET':
    artists = Artist.query.all()
    return render_template('artists.html', artists=artists)

# Albums routes
@app.route('/albums', methods=['POST', 'GET'])
def albums():
    if request.method == 'POST':
        data = request.form
        new_album = Album(title=data['title'], artist_id=data['artist_id'])
        db.session.add(new_album)
        db.session.commit()
        # return jsonify({'id': new_album.id, 'title': new_album.title, 'artist_id': new_album.artist_id}), 201
    # elif request.method == 'GET':
    albums = Album.query.all()
    artists = Artist.query.all()  # Fetch artists for dropdown
    return render_template('albums.html', albums=albums, artists=artists)

# Songs routes
@app.route('/songs', methods=['POST', 'GET'])
def songs():
    if request.method == 'POST':
        data = request.form
        new_song = Song(title=data['title'], artist_id=data['artist_id'], album_id=data.get('album_id'))
        db.session.add(new_song)
        db.session.commit()
        # return jsonify({'id': new_song.id, 'title': new_song.title, 'artist_id': new_song.artist_id, 'album_id': new_song.album_id}), 201
    # elif request.method == 'GET':
    songs = Song.query.all()
    artists = Artist.query.all()  # Fetch artists for dropdown
    albums = Album.query.all()    # Fetch albums for dropdown
    return render_template('songs.html', songs=songs, artists=artists, albums=albums)

if __name__ == '__main__':
    app.run(debug=True, extra_files=['templates/index.html', 'templates/artists.html', 'templates/albums.html', 'templates/songs.html','base.html'])
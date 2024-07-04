import os
from flask import Flask, request, jsonify, render_template, redirect
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from config import Config


app = Flask(__name__)
app.config.from_object(Config)
mongo = PyMongo(app)
db = mongo.db

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/artists', methods=['POST', 'GET'])
def artists():
    if request.method == 'POST':
        data = request.form
        new_artist = {'name': data['name']}
        db.artists.insert_one(new_artist)
        return redirect('/artists')
    artists = db.artists.find()
    return render_template('artists.html', artists=artists)

@app.route('/artists/<string:artist_id>', methods=['GET', 'POST'])
def update_artist(artist_id):
    artist = db.artists.find_one_or_404({'_id': ObjectId(artist_id)})
    
    if request.method == 'POST':
        db.artists.update_one({'_id': ObjectId(artist_id)}, {'$set': {'name': request.form['name']}})
        return redirect('/artists')
    
    return render_template('update_artist.html', artist=artist)

@app.route('/artists/<string:artist_id>/delete', methods=['POST'])
def delete_artist(artist_id):
    db.artists.delete_one({'_id': ObjectId(artist_id)})
    return redirect('/artists')


@app.route('/albums', methods=['POST', 'GET'])
def albums():
    if request.method == 'POST':
        data = request.form
        new_album = {'title': data['title'], 'artist_id': ObjectId(data['artist_id'])}
        db.albums.insert_one(new_album)
        return redirect('/albums')
    albums = db.albums.find()
    artists = db.artists.find()  
    return render_template('albums.html', albums=albums, artists=artists, db=db)

@app.route('/albums/<string:album_id>', methods=['GET', 'POST'])
def update_album(album_id):
    album = db.albums.find_one_or_404({'_id': ObjectId(album_id)})
    artists = db.artists.find()  
    
    if request.method == 'POST':
        db.albums.update_one({'_id': ObjectId(album_id)}, {'$set': {'title': request.form['title'], 'artist_id': ObjectId(request.form['artist_id'])}})
        return redirect('/albums')
    
    return render_template('update_album.html', album=album, artists=artists)

@app.route('/albums/<string:album_id>/delete', methods=['POST'])
def delete_album(album_id):
    db.albums.delete_one({'_id': ObjectId(album_id)})
    return redirect('/albums')


@app.route('/songs', methods=['POST', 'GET'])
def songs():
    if request.method == 'POST':
        data = request.form
        new_song = {'title': data['title'], 'artist_id': ObjectId(data['artist_id']), 'album_id': ObjectId(data.get('album_id'))}
        db.songs.insert_one(new_song)
        return redirect('/songs')
    songs = db.songs.find()
    artists = db.artists.find()  
    albums = db.albums.find()    
    return render_template('songs.html', songs=songs, artists=artists, albums=albums, db=db)

@app.route('/songs/<string:song_id>', methods=['GET', 'POST'])
def update_song(song_id):
    song = db.songs.find_one_or_404({'_id': ObjectId(song_id)})
    artists = db.artists.find()  
    albums = db.albums.find()    
    
    if request.method == 'POST':
        db.songs.update_one({'_id': ObjectId(song_id)}, {'$set': {'title': request.form['title'], 'artist_id': ObjectId(request.form['artist_id']), 'album_id': ObjectId(request.form.get('album_id'))}})
        return redirect('/songs')
    
    return render_template('update_song.html', song=song, artists=artists, albums=albums)

@app.route('/songs/<string:song_id>/delete', methods=['POST'])
def delete_song(song_id):
    db.songs.delete_one({'_id': ObjectId(song_id)})
    return redirect('/songs')


if __name__ == '__main__':
    app.run(host=os.getenv('FLASK_RUN_HOST', '0.0.0.0'), port=int(os.getenv('FLASK_RUN_PORT', 5000)))

from mongoengine import Document, fields

class Artist(Document):
    name = fields.StringField(required=True)

class Album(Document):
    title = fields.StringField(required=True)
    artist_id = fields.ReferenceField(Artist, required=True)

class Song(Document):
    title = fields.StringField(required=True)
    artist_id = fields.ReferenceField(Artist, required=True)
    album_id = fields.ReferenceField(Album, required=False)

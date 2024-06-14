import os

class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'postgresql://music_user:postgres@localhost/music_publisher')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
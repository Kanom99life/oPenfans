from datetime import datetime
from app import db
from sqlalchemy_serializer import SerializerMixin

class BlogEntry(db.Model, SerializerMixin):
    __tablename__ = "blogentry"

    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.String(280))
    date_created = db.Column(db.DateTime)
    date_update = db.Column(db.DateTime)
    avatar_url = db.Column(db.String(300))
    img = db.Column(db.String(1000), nullable=True)
    
    def __init__(self, message, avatar_url, img=None):
        self.message = message   
        self.date_created = datetime.now()
        self.date_update = datetime.now()
        self.avatar_url = avatar_url
        self.img = img

        
    def update(self, message, avatar_url, img=None):
        self.message = message
        self.date_update = datetime.now()
        self.avatar_url = avatar_url
        self.img = img
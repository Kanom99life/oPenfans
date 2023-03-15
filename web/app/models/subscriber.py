from app import db
from sqlalchemy_serializer import SerializerMixin

class Subscribe(db.Model, SerializerMixin):
    __tablename__ = "subscribe"

    id = db.Column(db.Integer, primary_key=True)
    user_sub = db.Column(db.Integer)
    sub_owner = db.Column(db.Integer)
    
    def __init__(self, user_sub, sub_owner):
        self.user_sub = user_sub
        self.sub_owner = sub_owner

        
    def update(self, user_sub, sub_owner):
        self.user_sub = user_sub
        self.sub_owner = sub_owner
from app import db

class Item(db.Model):
    __tablename__ = 'item'
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    name = db.Column(db.String)

from app import db 
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.Integer, index=True)
    name = db.Column(db.String(64))
    number = db.Column(db.String(64))
    contacts = db.Column(db.String(128))
    numbers = db.Column(db.String(128))
    location_url = db.Column(db.String(128), default='NA')

    def __repr__(self):
        return '<User {} {} {} {} {} {} {}>'.format(self.id, self.key, self.name, self.number, self.location_url, self.contacts, self.numbers)


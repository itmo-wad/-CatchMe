from app import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    token = db.Column(db.String, unique=True)

    def __init__(self, token):
        self.token = token

    def __repr__(self):
        return '<User %r>' % self.token

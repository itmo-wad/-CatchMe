from app import db


class WebSiteAdmin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(80), unique=True)
    username = db.Column(db.String(120), unique=True)
    passwdhash = db.Column(db.String, unique=False)
    token = db.Column(db.String, unique=True)

    def __init__(self, email, username):
        self.username = username
        self.email = email

    def __repr__(self):
        return '<User %r>' % self.username

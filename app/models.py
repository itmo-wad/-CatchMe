from app import db


class Visitor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    token = db.Column(db.String, unique=True)
    username = db.Column(db.String(120), unique=False)

    def __repr__(self):
        return "{'User' : [id='%s', token='%s', username='%s']}" % (self.id, self.token, self.username)


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    parent_id = db.Column(db.Integer, unique=False)
    web_site_admin_id = db.Column(db.Integer, db.ForeignKey('web_site_admin.id'))
    visitor_id = db.Column(db.Integer, db.ForeignKey('visitor.id'), nullable=False)
    what_is_commented_id = db.Column(db.Integer, unique=False)
    comment_text = db.Column(db.String(128))

    visitor = db.relationship('Visitor',
                               backref=db.backref('comments', lazy=True))

    web_site_admin = db.relationship('WebSiteAdmin',
                              backref=db.backref('web_admins', lazy=True))

    def __repr__(self):
        return '<Comment_id: %s, comment_text: %s>' % (self.id, self.comment_text)


class WebSiteAdmin(db.Model):
    db.__tablename__ = "web_site_admin"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(80), unique=True)
    username = db.Column(db.String(120), unique=True)
    passwdhash = db.Column(db.String, unique=False)
    token = db.Column(db.String, unique=True)

    def __repr__(self):
        return '<User %r>' % self.username

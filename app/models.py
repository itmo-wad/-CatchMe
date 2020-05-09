from app import db


class Visitor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    token = db.Column(db.String, unique=True)
    username = db.Column(db.String(120), unique=False)

    # def __init__(self, token):
    #     self.token = token

    def __repr__(self):
        return '<User %r>' % self.token

    def set_username(self, username):
        self.username = username


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

    # def __init__(self, parent_id, web_site_admin_id, user_id, what_is_commented_id, comment_text):
    #     self.parent_id = parent_id
    #     self.web_site_admin_id = web_site_admin_id
    #     self.user_id = user_id
    #     self.what_is_commented_id = what_is_commented_id
    #     self.comment_text = comment_text

    def __repr__(self):
        return '<Comment_text: %s>' % self.comment_text


class WebSiteAdmin(db.Model):
    db.__tablename__ = "web_site_admin"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(80), unique=True)
    username = db.Column(db.String(120), unique=True)
    passwdhash = db.Column(db.String, unique=False)
    token = db.Column(db.String, unique=True)

    # def __init__(self, email, username):
    #     self.username = username
    #     self.email = email

    def __repr__(self):
        return '<User %r>' % self.username

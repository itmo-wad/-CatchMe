from app import db


class Comments(db.Model):
    __tablename__ = 'comments'
    Id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    ParentId = db.Column(db.Integer)
    SiteAdminId = db.Column(db.Integer, db.ForeignKey('siteadmins.Id'), nullable=False)
    Username = db.Column(db.String(16), nullable=False)
    CommentObjectId = db.Column(db.Integer, nullable=False)
    CommentText = db.Column(db.String(256))

    SiteAdmin = db.relationship('SiteAdmins',
                            backref=db.backref('comment', lazy=True))

    def __repr__(self):
        return "{'Comment' : [id='%s', parent_id='%s', site_admin_id='%s', username='%s', CommentObjectId='%s', " \
               "CommentText='%s']}" % (self.Id, self.ParentId, self.SiteAdminId, self.Username, self.CommentObjectId,
                                       self.CommentText)


class SiteAdmins(db.Model):
    __tablename__ = 'siteadmins'
    Id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Email = db.Column(db.String(32), unique=True)
    Username = db.Column(db.String(16), unique=True)
    Passwdhash = db.Column(db.String, unique=False)

    def __repr__(self):
        return "{'SiteAdmin' : [id='%s', email='%s', username='%s']}" % \
               (self.Id, self.Email, self.Username)


class Tokens(db.Model):
    __tablename__ = 'tokens'
    Id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    TokenValue = db.Column(db.String, unique=False, nullable=False)
    Status = db.Column(db.Boolean, unique=False, nullable=False)
    SiteAdminId = db.Column(db.Integer, db.ForeignKey('siteadmins.Id'), nullable=False)

    SiteAdmin = db.relationship('SiteAdmins',
                               backref=db.backref('token', lazy=True, uselist=False))

    def __repr__(self):
        return "{'Tokens' : [id='%s', token_value='%s' status='%s', site_admin_id='%s']}" % \
               (self.Id, self.TokenValue, self.Status, self.SiteAdminId)

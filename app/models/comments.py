from app import db


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    comment_text = db.Column(db.String(128))
    parent_id = db.Column(db.Integer, unique=False)
    web_site_admin_id = db.Column(db.Integer, unique=False)
    user_id = db.Column(db.Integer, unique=False)
    what_is_commented = db.Column(db.Integer, unique=False)

    def __init__(self, comment_text, parent_id, web_site_admin_id, user_id, what_is_commented):
        self.comment_text = comment_text
        self.parent_id = parent_id
        self.web_site_admin_id = web_site_admin_id
        self.user_id = user_id
        self.what_is_commented = what_is_commented

    def __repr__(self):
        return '<>' % self.comment_text

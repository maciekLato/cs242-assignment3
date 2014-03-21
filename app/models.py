from app import db

ROLE_USER = 0
ROLE_ADMIN = 1

class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(64), index = True, unique = True)
    role = db.Column(db.SmallInteger, default = ROLE_USER)

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return unicode(self.id)

    def __repr__(self):
        return '<User %r>' % (self.username)

class Project(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	projectname = db.Column(db.String(64), index = True, unique = True)

class Comment(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	content = db.Column(db.String(200))
	timestamp = db.Column(db.DateTime)
	user_name = db.Column(db.String(50))
	project_name = db.Column(db.String(50))

	def __repr__(self):
		return '<Post %r>' % (self.content)
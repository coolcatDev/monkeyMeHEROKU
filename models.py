from app import db
#from sqlalchemy.dialects.postgresql import JSON

class users(db.Model):

	__tablename__ = "Users"

	id = db.Column(db.Integer, primary_key=True)
	userName = db.Column(db.String, nullable=False)
	userEmail = db.Column(db.String, nullable=False)
	userPhone = db.Column(db.String, nullable=False)
	userPass = db.Column(db.String, nullable=False)

	def __init__(self, userName, userEmail, userPhone, userPass):
		
		self.userName = userName
		self.userEmail = userEmail
		self.userPhone = userPhone
		self.userPass = userPass
		
	def __repr__(self):
		return '{}-{}-{}-{}'.format(self.id, self.userName, self.userEmail, self.userPhone)




class friendships(db.Model):

	__tablename__ = "Friendships"

	id = db.Column(db.Integer, primary_key=True)
	userIdA = db.Column(db.Integer, nullable=False)
	userIdB = db.Column(db.Integer, nullable=False)
	userNameA = db.Column(db.String, nullable=False)
	userNameB = db.Column(db.String, nullable=False)



	def __init__(self, userIdA, userIdB, userNameA, userNameB):
	
		
		self.userIdA = userIdA
		self.userIdB = userIdB
		self.userNameA = userNameA
		self.userNameB = userNameB
	
		
	def __repr__(self):
		return '{}-{}-{}-{}'.format(self.userIdA, self.userIdB, self.userNameA, self.userNameB)



class bestFriends(db.Model):

	__tablename__ = "BestFriends"

	id = db.Column(db.Integer, primary_key=True)
	userIdA = db.Column(db.Integer, nullable=False)
	userIdB = db.Column(db.Integer, nullable=False)
	userNameA = db.Column(db.String, nullable=False)
	userNameB = db.Column(db.String, nullable=False)

	

	def __init__(self, userIdA, userIdB, userNameA, userNameB):
		
		self.userIdA = userIdA
		self.userIdB = userIdB
		self.userNameA = userNameA
		self.userNameB = userNameB
	
		
	def __repr__(self):
		return '{}-{}-{}-{}'.format(self.userIdA, self.userIdB, self.userNameA, self.userNameB)
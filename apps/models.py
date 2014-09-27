from apps import db

class User(db.Model):
	no = db.Column(db.Integer, primary_key=True, autoincrement=True)
	email = db.Column(db.String(127), unique=True)
	password = db.Column(db.String(127))
	name = db.Column(db.String(10))

class Store(db.Model):
	no = db.Column(db.Integer, primary_key=True, autoincrement=True)
	owner = db.Column(db.Integer, db.ForeignKey('user.no'))
	name = db.Column(db.String(10))

class Stock(db.Model):
	no = db.Column(db.Integer, primary_key=True, autoincrement=True)
	owner = db.Column(db.Integer, db.ForeignKey('store.no'))
	category = db.Column(db.Integer, db.ForeignKey('category.no'))
	name = db.Column(db.String(50))
	size = db.Column(db.String(20))
	stock = db.Column(db.Integer)
	unitcost = db.Column(db.Integer)
	memo = db.Column(db.String(1000))

class Category(db.Model):
	no = db.Column(db.Integer, primary_key=True, autoincrement=True)
	name = db.Column(db.String(20))

class History(db.Model):
	no = db.Column(db.Integer, primary_key=True, autoincrement=True)
	owner = db.Column(db.Integer, db.ForeignKey('stock.no'))
	date_created = db.Column(db.Date)
	totalin = db.Column(db.Integer)
	totalout = db.Column(db.Integer)
	totalstock = db.Column(db.Integer)

class Inout(db.Model):
	no = db.Column(db.Integer, primary_key=True, autoincrement=True)
	owner = db.Column(db.Integer, db.ForeignKey('history.no'))
	date_created = db.Column(db.Date)
	tin = db.Column(db.Integer)
	tout = db.Column(db.Integer)
	tstock = db.Column(db.Integer)
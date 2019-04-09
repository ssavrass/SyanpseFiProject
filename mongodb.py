import pymongo as pm

class MongoDB():
	def __init__(self):
		conn = pm.MongoClient("localhost", 27017)
		db = conn.synapsefi
		self.users = db.users
	def add_user(self, userid, name, email, phone):
		self.users.insert({'id':userid,'name':name, 'email':email, 'phone':phone, 'deposit_node':None, 'recipient_nodes':[], 'transactions':[]})
	def add_deposit_node(self, userid, body):
		self.users.update({'id':userid}, {'$set':{'deposit_node':body}})
	def add_recipient_node(self, userid, body):
		existing = self.users.find({'id':userid})[0]['recipient_nodes']
		existing.append(body)
		self.users.update({'id':userid}, {'$set':{'recipient_nodes':existing}})
	def add_transaction(self, userid, body):
		existing = self.users.find({'id':userid})[0]['transactions']
		existing.append(body)
		self.users.update({'id':userid}, {'$set':{'transactions':existing}})
	def view_user(self, userid):
		return self.users.find({'id':userid})[0]
	def view_recipient_node(self, userid, _id):
		try:
			nodes = self.users.find({'id':userid})[0]['recipient_nodes']
			for el in nodes:
				if el['_id'] == _id:
					return el
		except:
			return None
	def view_all_recipient_nodes(self, userid):
		nodes = self.users.find({'id':userid})[0]['recipient_nodes']
		return nodes
	def view_transaction(self, userid, _id):
		try:
			transactions = self.users.find({'id':userid})[0]['transactions']
			for el in transactions:
				if el['_id'] == _id:
					return el
		except:
			return None
	def view_all_transactions(self, userid):
		try:
			transactions = self.users.find({'id':userid})[0]['transactions']
			return transactions
		except:
			return None
		

# def run():
# 	db = MongoDB()
# 	db.add_user(123, "Sergey Savrasov", "ssavrass@gmail.com", "530-902-6441")
# 	print(db.view_user(123))
# 	db.add_deposit_node(123,{'_id':5})
# 	db.add_recipient_node(123,{'_id':7})
# 	db.add_transaction(123,{'_id':3})
# 	db.add_transaction(123,{'_id':4})
# 	db.add_transaction(123,{'_id':5})
# 	db.add_transaction(123,{'_id':6})
# 	print(db.view_recipient_node(123,7))
# 	print(db.view_user(123))
# 	print(db.view_all_transactions(123))
# 	db.users.remove()

	




# run()
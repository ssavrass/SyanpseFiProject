import os
from synapsepy import Client
client = Client('client_id_4dOQ80pG2K5XZyt9SENF0e7Rv6ITnHWAqJh3wrsC', 'client_secret_7QyI0Oamnz2HMCZVP3KvoeWTDj1658gFcLpsfkrY', 
	'USER_FINGERPRINT',
    '127.0.0.1',
    True, 
    False 
)

class User():
	def __init__(self, email, phone, name):
		self.users = []
		self.ip = '127.0.0.1'
		body = {
		  "logins": [
		    {
		      "email": email
		    }
		  ],
		  "phone_numbers": [
		   phone
		  ],
		  "legal_names": [
		    name
		  ],
		  "extra": {
		    "supp_id": "122eddfgbeafrfvbbb",
		    "cip_tag":1,
		    "is_business": False
		  }
		}
		self.user = client.create_user(body, self.ip)
		self.body = self.user.body
		self.oauth()


	def oauth(self):
		
		body = {
		    "refresh_token":self.user.body['refresh_token'],
		    "scope":[
		        "NODES|POST",
		        "NODES|GET",
		        "NODE|GET",
		        "TRANS|POST",
		        "USER|PATCH",
        		"USER|GET"
    			]
    		}
		return self.user.oauth(body)
	
	def view_user(self, user_id):
		return client.get_user(user_id, full_dehydrate=True)

class CheckDeposit():
	
	def __init__(self, user):
		self.dic = {}
		body= {
		   "type": "DEPOSIT-US",
		   "info": {
		      "nickname": "My Deposit Account"
		      
		   }
		}
		self.deposit = user.create_node(body)
		self.deposit_id = self.deposit.list_of_nodes[0].body['_id']
	
	def create_new_recipient(self, user, nickname, payee_name, street,city,state,country,zip_code):
		body = {
		  "type": "CHECK-US",
		  "info":{
		      "nickname":nickname,
		      "payee_name":payee_name,
		      "payee_address":{
		        "address_street":street,
		        "address_city":city,
		        "address_subdivision":state,
		        "address_country_code":country,
		        "address_postal_code":zip_code
				}
			}
		}
		node = user.create_node(body)
		self.dic[payee_name] = node.list_of_nodes[0].body['_id']
		return node.list_of_nodes[0]

	def send_check(self, user, from_node_id, to_node_id, amount, currency, ip, note):
		body = {
		  "to": {
		    "type": 'CHECK-US',
		    "id": to_node_id
		  },
		  
		  "amount": {
		    "amount": amount,
		    "currency": currency
		  },
		  "extra": {
		    "ip": ip,
		    "note": note
		  }
		}
		
		return user.create_trans(from_node_id, body)

# def run():
# 	a = Users()
# 	a.create_user('ssavrass@gmail.com', '(530) 902-6441', 'Sergey Savrasov')
# 	print(a.users)
# 	user = a.view_user(a.users[0])
# 	print(a.oauth(user))
# 	print(user.body)
# 	print('__________________________________________')
# 	b = CheckDeposit(user)
# 	print(b.deposit.list_of_nodes[0].body)
# 	print('__________________________________________')
# 	node = b.create_new_recipient(user, "CHECK-US", "student loan", "EDD", "1 Market St", "San Francisco", "CA", "US", "94105")
# 	print(node.list_of_nodes[0].body)
# 	node_id = (node.list_of_nodes[0].body['_id'])
# 	print(node_id)
# 	print('__________________________________________')
# 	print(b.send_check(user, b.deposit_id, b.dic['student loan'], 100, 'USD', a.ip, 'TEST').body)	
	
# run()


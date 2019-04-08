from wtforms import Form, StringField, validators

class DepositForm(Form):
    name = StringField('Name',[validators.Length(min=1)])
    email = StringField('Email', [validators.Length(min=1)])
    phone = StringField('Phone', [validators.Length(min=1)])

class RecipientForm(Form):
    nick_name = StringField('Nick Name',[validators.Length(min=1)])
    payee_name = StringField('Payee Name', [validators.Length(min=1)])
    street = StringField('Street', [validators.Length(min=1)])
    city = StringField('City', [validators.Length(min=1)])
    state = StringField('State', [validators.Length(min=1)])
    country = StringField('Country', [validators.Length(min=1)])
    zip_code = StringField('Zip Code', [validators.Length(min=1)])

class CheckForm(Form):
	amount = StringField('Amount',[validators.Length(min=1)])
	currency = StringField('Currency',[validators.Length(min=1)])
	note = StringField('Note',[validators.Length(min=1)])

class DepositDetails():
	
	def __init__(self, name, email, phone, _id, body):

		self.name = name
		self.email = email
		self.phone = phone
		self._id = _id
		self.body = body

class RecipientDetails():
	recipients = []
	def __init__(self,nick_name,payee_name,street,city,state,country,zip_code,_id,body):
	    self.nick_name = nick_name
	    self.payee_name = payee_name
	    self.street = street
	    self.city = city
	    self.state = state
	    self.country = country
	    self.zip_code = zip_code
	    self._id = _id
	    self.body = body
	    RecipientDetails.recipients.append(self)

class CheckDetails():
	checks = []
	def __init__(self, to, amount, currency, note, _id, body):
		self.to = to
		self.amount = amount
		self.currency = currency
		self.note = note
		self.id = _id
		self.body = body
		CheckDetails.checks.append(self)



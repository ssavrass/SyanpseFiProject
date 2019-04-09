from flask import Flask, request, render_template, redirect, url_for, flash
app = Flask(__name__)
app.secret_key = b'dsfkjdskfjdskfj'

from .forms import DepositForm, DepositDetails, RecipientForm, RecipientDetails, CheckForm, CheckDetails
from .synapsefi import User, CheckDeposit

@app.route('/', methods=['GET', 'POST'])
def index():
  form = DepositForm(request.form)
  if request.method == 'POST' and form.validate():
      name = request.form['name']
      email = request.form['email']
      phone = request.form['phone']
      global new_user
      new_user = User(email,phone,name)
      global deposit_details
      deposit_details = DepositDetails(name,email,phone,new_user.user.id,new_user.body)
      global new_deposit_account
      new_deposit_account = CheckDeposit(new_user.user)
      return redirect(url_for('myaccount'))
  return render_template('index.html', form=form)


@app.route('/myaccount', methods=['GET', 'POST'])
def myaccount(): 
  form = RecipientForm(request.form)
  recipients = deposit_details.db.view_all_recipient_nodes(new_user.user.id)
 
  if request.method == 'POST' and form.validate():
      nick_name = request.form['nick_name']
      payee_name = request.form['payee_name']
      street = request.form['street']
      city = request.form['city']
      state = request.form['state']
      country = request.form['country']
      zip_code = request.form['zip_code']
      try:
        new_node = new_deposit_account.create_new_recipient(new_user.user, nick_name,payee_name,street,city,state,country,zip_code)
      except Exception as e: 
        flash(e.message)
        return redirect(url_for('myaccount'))
      recipient_details_new = RecipientDetails(nick_name,payee_name,street,city,state,country,zip_code, new_node.id,new_node.body)
      deposit_details.db.add_recipient_node(new_user.user.id, new_node.body)
      
      recipients = deposit_details.db.view_all_recipient_nodes(new_user.user.id)
      
      return render_template('myaccount.html', form=form, deposit_details=deposit_details, recipients=recipients)
  return render_template('myaccount.html', form=form, deposit_details=deposit_details, recipients=recipients)

@app.route('/recipient/<name>', methods=['GET', 'POST'])
def recipient(name=None):
  form = CheckForm(request.form)
  check_details = deposit_details.db.view_all_transactions(new_user.user.id)
  if request.method == 'POST' and form.validate():
    to = name
    amount = request.form['amount']
    currency= request.form['currency']
    note = request.form['note']
    new_check = new_deposit_account.send_check(new_user.user, new_deposit_account.deposit_id, new_deposit_account.dic[name], amount, currency, new_user.ip, note)
    check_details_new = CheckDetails(to, amount, currency, note, new_check.id, new_check.body)
    deposit_details.db.add_transaction(new_user.user.id, new_check.body)
    check_details = deposit_details.db.view_all_transactions(new_user.user.id)
    return render_template('recipient.html', name=name, form=form, check_details=check_details)
  return render_template('recipient.html', name=name, form=form, check_details=check_details)


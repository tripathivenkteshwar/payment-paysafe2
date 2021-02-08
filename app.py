from flask import Flask, render_template, request
from payment import create_customer, merchantRefNum
from payment import pay_for_product, single_use_token

from flask_sqlalchemy import SQLAlchemy
from user import user

from os import environ
#from dotenv import load_dotenv


#basedir = path.abspath(path.dirname(__file__))
#load_dotenv(path.join(basedir, '.env'))
SECRET_KEY = environ.get('SECRET_KEY')

user_info = user()

app = Flask(__name__)

#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///check_db.db'
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('DATABASE_URL')

db = SQLAlchemy(app)
class check(db.Model):
    email = db.Column('email', db.String, primary_key = True)
    customerId = db.Column(db.String(100), nullable=False)


    def __repr__(self):
        return f"User('{self.email}', '{self.customerId}')"

@app.route('/')
def paysafe():
    return render_template('Payment_Form.html')

@app.route('/single_User', methods=['POST'])
def single_User():

    user_info.mer_ref = merchantRefNum()
    data = request.get_json()
    print("hello")
    ch = check.query.filter_by(email=data['email']).first()
    print(ch)

    if ch:
        #customer already present
        user_info.cust_id=ch.customerId
    else:

        cust = create_customer(data, user_info.mer_ref, SECRET_KEY)
        user_info.cust_id = cust['id']
        create_cust=check(email=data['email'], customerId=cust['id'])
        db.session.add(create_cust)
        db.session.commit()

    #cust = create_customer(data, user_info.mer_ref, SECRET_KEY)
    #user_info.cust_id = cust['id']

    single_tok = single_use_token(user_info.cust_id, user_info.mer_ref, SECRET_KEY)

    if single_tok['status']=="ACTIVE":
        return {
            'status': 'OK',
            'data':{
                'merchantRefNum': user_info.mer_ref,
                'singleUseCustomerToken': single_tok['singleUseCustomerToken']
            }
        }
    else:
        return {
            'status':"NO",
            'data':None
        }

@app.route('/payment_process', methods=['POST'])
def payment_process():
    data = request.get_json()
    paymentHandleToken = data['paymentHandleToken']
    amount=data['amount']
    pay = pay_for_product(paymentHandleToken, amount, user_info.mer_ref, SECRET_KEY)
    if pay and "status" in pay and pay["status"] == "COMPLETED":
        return {'status':"OK", 'data':pay}
    else:
        return {'status':"NO", 'data':pay}


if __name__ == '__main__':
    app.run()

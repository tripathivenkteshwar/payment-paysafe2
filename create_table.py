from flask import Flask
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] =environ.get('DATABASE_URL')


db = SQLAlchemy(app)
class check(db.Model):
    email = db.Column('email', db.String, primary_key = True)
    customerId = db.Column(db.String(100), nullable=False)


    def __repr__(self):
        return f"User('{self.email}', '{self.customerId}')"
db.create_all()




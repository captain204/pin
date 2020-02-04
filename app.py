from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy 
from flask_marshmallow import Marshmallow 
import string
import os
import random

# Init app
app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
# Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'db.pin')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# Init db
db = SQLAlchemy(app)
# Init ma
ma = Marshmallow(app)

class Pin(db.Model):
  
  id = db.Column(db.Integer, primary_key=True)
  pin = db.Column(db.String(15), unique=True)
  serial_no = db.Column(db.String(12), unique=True)

  def __init__(self, pin, serial_no):
    self.pin = pin
    self.serial_no = serial_no


#Pin Schima
class PinSchema(ma.Schema):
      class Meta:
        fields = ('id', 'pin', 'serial_no')

# Init schema
pin_schema = PinSchema()
pins_schema = PinSchema(many=True)



# Generate  pin
@app.route('/api/v1/generate', methods=['GET'])
def add_pin():
  #serial_default =0000000000
  pin = ''.join([random.choice(string.digits) for n in range (15)])
  serial_no = ''.join([random.choice(string.digits) for n in range (12)])
  new_pin = Pin(pin, serial_no)
  db.session.add(new_pin)
  db.session.commit()
  return pin_schema.jsonify(new_pin)

  


# Get All Pins
@app.route('/pin', methods=['GET'])
def get_pins():
  all_pins = Pin.query.all()
  result = pins_schema.dump(all_pins)
  return jsonify(result.data)

# Get Single Pin
@app.route('/api/v1/validate/<serial>', methods=['GET'])
def get_pin(serial):
  check = Pin.query.filter_by(serial_no = serial).first()
  
  if check:
        return jsonify({'message':'1'})
  else:
        return jsonify({'message':'0'})






# Run Server
if __name__ == '__main__':
  app.run(debug=True)
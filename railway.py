from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///railway.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Train(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    source = db.Column(db.String(50), nullable=False)
    destination = db.Column(db.String(50), nullable=False)
    departure_time = db.Column(db.String(50), nullable=False)
    arrival_time = db.Column(db.String(50), nullable=False)

class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    passenger_name = db.Column(db.String(100), nullable=False)
    train_id = db.Column(db.Integer, db.ForeignKey('train.id'), nullable=False)

@app.before_first_request
def create_tables():
    db.create_all()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/trains', methods=['GET'])
def get_trains():
    trains = Train.query.all()
    output = []
    for train in trains:
        train_data = {
            'id': train.id,
            'name': train.name,
            'source': train.source,
            'destination': train.destination,
            'departure_time': train.departure_time,
            'arrival_time': train.arrival_time
        }
        output.append(train_data)
    return jsonify(output)

@app.route('/book', methods=['POST'])
def book_ticket():
    data = request.get_json()
    passenger_name = data['passenger_name']
    train_id = data['train_id']

    train = Train.query.get(train_id)
    if not train:
        return jsonify({'message': 'Train not found'}), 404

    booking = Booking(passenger_name=passenger_name, train_id=train_id)
    db.session.add(booking)
    db.session.commit()
    return jsonify({'message': 'Ticket booked successfully'})

@app.route('/bookings', methods=['GET'])
def get_bookings():
    bookings = Booking.query.all()
    output = []
    for booking in bookings:
        booking_data = {
            'id': booking.id,
            'passenger_name': booking.passenger_name,
            'train_id': booking.train_id
        }
        output.append(booking_data)
    return jsonify(output)

@app.route('/add_train', methods=['POST'])
def add_train():
    data = request.get_json()
    train = Train(
        name=data['name'],
        source=data['source'],
        destination=data['destination'],
        departure_time=data['departure_time'],
        arrival_time=data['arrival_time']
    )
    db.session.add(train)
    db.session.commit()
    return jsonify({'message': 'Train added successfully'})

@app.route('/delete_train/<int:id>', methods=['DELETE'])
def delete_train(id):
    train = Train.query.get(id)
    if not train:
        return jsonify({'message': 'Train not found'}), 404
    db.session.delete(train)
    db.session.commit()
    return jsonify({'message': 'Train deleted successfully'})

if __name__ == '__main__':
    app.run(debug=True)

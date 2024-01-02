from flask import Flask, request, jsonify, abort
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Configure the database URL (replace with your database URL)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///house.db'

# Initialize the SQLAlchemy database
db = SQLAlchemy(app)


# Define the House model
class House(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    house_type = db.Column(db.String(255), nullable=False)
    bargain_type = db.Column(db.String(255))
    city = db.Column(db.String(255), nullable=False)
    region = db.Column(db.String(255), nullable=False)
    area = db.Column(db.Integer, nullable=False)
    building_year = db.Column(db.Integer)
    floor = db.Column(db.Integer)
    title_deeds = db.Column(db.String(255))
    elevator = db.Column(db.Boolean)
    parking = db.Column(db.Boolean)
    store_room = db.Column(db.Boolean)
    price = db.Column(db.Integer, nullable=False)

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


# Route for creating a new house
@app.route('/houses', methods=['POST'])
def create_house():
    data = request.json
    house = House(**data)
    db.session.add(house)
    db.session.commit()
    return jsonify({'message': 'House created successfully', 'house': house.as_dict()}), 201


# Route for retrieving a specific house by ID
@app.route('/houses/<int:id>', methods=['GET'])
def get_house(id):
    house = House.query.get(id)
    if house is None:
        abort(404, description='House not found')
    return jsonify(house.as_dict())


# Route for updating a specific house by ID
@app.route('/houses/<int:id>', methods=['PUT'])
def update_house(id):
    house = House.query.get(id)
    if house is None:
        abort(404, description='House not found')

    data = request.json
    for key, value in data.items():
        setattr(house, key, value)

    db.session.commit()
    return jsonify({'message': 'House updated successfully', 'house': house.as_dict()})


# Route for deleting a specific house by ID
@app.route('/houses/<int:id>', methods=['DELETE'])
def delete_house(id):
    house = House.query.get(id)
    if house is None:
        abort(404, description='House not found')

    db.session.delete(house)
    db.session.commit()
    return jsonify({'message': 'House deleted successfully'})


if __name__ == '__main__':
    # Create the database tables
    db.create_all()
    app.run(debug=True)
# server/app.py
#!/usr/bin/env python3

from flask import Flask, make_response, jsonify 
from flask_migrate import Migrate

from models import db, Earthquake

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)


@app.route('/')
def index():
    body = {'message': 'Flask SQLAlchemy Lab 1'}
    return make_response(body, 200)

# Add views here
@app.route('/earthquakes/<int:id>')
def id_route(id):
    match = Earthquake.query.filter_by(id=id).first()
    if match:
        body = {'id':match.id,
                'location':match.location,
                'magnitude':match.magnitude,
                'year':match.year
                }
        return make_response(jsonify(body), 200)
    else:
        body = {"message": f"Earthquake {id} not found."}
        return make_response(jsonify(body), 404)


@app.route('/earthquakes/magnitude/<float:magnitude>')
def magnitude_query(magnitude):
    queried = Earthquake.query.filter(Earthquake.magnitude>=magnitude).all()
    quakes = [
            {
                'id': q.id,
                'location': q.location,
                'magnitude': q.magnitude,
                'year': q.year
            }
            for q in queried
        ]
    count = len(quakes)

    if queried:
       body = {
            'count': count,
            'quakes': quakes
        }
       
       return make_response(jsonify(body),200)
    else:
       body = {
            'count': 0,
            'quakes': []
        }
       return make_response(jsonify(body),200)

if __name__ == '__main__':
    app.run(port=5555, debug=True)

from flask import render_template, session, abort, request, jsonify, redirect
from app import app, db
from app.models import User
from uuid import uuid4
import json


@app.route('/')
def index():
    return render_template('index.html') 


@app.route('/api/user', methods=['POST'])
def create_user():
    name = request.json.get('name')
    number = request.json.get('number')
    key = uuid4().hex 

    new_user = User(name=name, number=number, key=key)
    db.session.add(new_user)
    db.session.commit()

    response = {
            'status': 'Successful',
            'key': new_user.key,
            'id': new_user.id
    }

    print(new_user);
    return jsonify(response) 

@app.route('/api/user/contacts', methods=['POST'])
def add_contacts():
    key = request.json.get('key')
    user = User.query.filter_by(key=key).first()
    if user is None:
        abort(404)

    user.contacts = request.json.get('names')
    user.numbers =  request.json.get('numbers')

    print(user)
    db.session.commit()

    response = dict()
    response['status'] = 'Success'

    return jsonify(response) 


@app.route('/api/user/contacts')
def get_contacts():
    key = response.json.get('key')
    user = User.query.filter_by(key=key).first()

    if user is None:
        abort(404)

    response = dict()
    response['status'] = 'Success'
    response['names'] = user.contacts
    response['numbers'] = user.numbers

    return jsoniry(response)
    

@app.route('/api/user/track', methods=['POST'])
def track_user():
    key = request.json.get('key')
    latitude = request.json.get('latitude')
    longitude = request.json.get('longitude')

    print(request.json)

    user = User.query.filter_by(key=key).first()
    response = dict()
    if user is None:
        response['status'] = 'User not found'
        return jsonify(response)

    google_map_url = 'https://www.google.com/maps/search/?api=1&query={},{}'.format(latitude, longitude)
    user.location_url  = google_map_url if latitude != None else 'NA'
    db.session.commit()

    response['status'] = 'Successful'
    return jsonify(response)


@app.route('/user/location')
def get_location():
    key = request.args.get('key')

    user = User.query.filter_by(key=key).first()
    if user is None:
        abort(404)

    google_map_url = user.location_url
    if google_map_url is 'NA':
        abort(404)

    return redirect(google_map_url)

@app.route('/users/viewall')
def view_users():
    users = User.query.all()

    user_html = str()
    for user in users:
        print(user)
        user_html += str(user)

    return user_html

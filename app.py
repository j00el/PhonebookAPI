from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os

#init app
app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
#Database
app.config['SQLALCHEMY_DATABASE_URI']='postgresql://postgres:Karma-crash123@localhost/phonebook'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#init DB
db = SQLAlchemy(app)
#init ma
ma = Marshmallow(app)

#Entry Class/Model
class Entry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30))
    number = db.Column(db.String(10), unique=True)

    def __init__(self, name, number):
        self.name = name
        self.number = number

# Entry Schema
class EntrySchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'number')

#init Schema
entry_schema = EntrySchema()
entrys_schema = EntrySchema(many=True)

#Create Phonebook Entry
@app.route('/entry', methods=['POST'])
def add_entry():
    name = request.json['name']
    number = request.json['number']

    new_entry = Entry(name, number)
    db.session.add(new_entry)
    db.session.commit()

    return entry_schema.jsonify(new_entry)

#Get All Phonebook Entrys
@app.route('/entry', methods=['GET'])
def getAllEntry():
    all_Entrys = Entry.query.all()
    result = entrys_schema.dump(all_Entrys)
    return jsonify(result)

#Get a Single Entry by ID
@app.route('/entry/<id>', methods=['GET'])
def getEntry(id):
    entry = Entry.query.get(id)
    return entry_schema.jsonify(entry)

#Update a Entry by ID
@app.route('/entry/<id>', methods=['PUT'])
def updateEntry(id):
    entry = Entry.query.get(id)
    name = request.json['name']
    number = request.json['number']
    entry.name = name
    entry.number = number
    db.session.commit()
    return entry_schema.jsonify(entry)

#Delte a Entry by ID
@app.route('/entry/<id>', methods=['DELETE'])
def deleteEntry(id):
    entry = Entry.query.get(id)
    db.session.delete(entry)
    db.session.commit()
    return entry_schema.jsonify(entry)

#Run Server
if __name__ == '__main__':
    app.run(debug=True)

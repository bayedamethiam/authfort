from flask import Flask, request, Response, jsonify,render_template
from apscheduler.schedulers.background import BackgroundScheduler

import json
from json import JSONEncoder
import urllib.request

from flask import  redirect, request, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy import desc, func, text
from datetime import datetime
import os



app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
#'postgresql://postgres:bayedame@127.0.0.1:5432/postgres'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'jknjknc6v468v86v354'

#port = int(os.environ["PORT"])

db = SQLAlchemy(app)
migrate = Migrate()
migrate.init_app(app, db)






class Utilisateur(db.Model):

    __tablename__ = 'utilisateur'
    id=db.Column(db.Integer, primary_key=True)
    image_reference=db.Column(db.String(60))
    qr_reference = db.Column(db.String(60))
    rfid_reference=db.Column(db.String(60))
 


    def __repr__(self):
        return '<utilisateur: {}>'.format(self.id)

class Historique(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    action =db.Column(db.String(80))
    date=db.Column(db.DateTime)
    utilisateur=db.Column(db.Integer)

    def __repr__(self):
        return '<utilisateur: {}>'.format(self.id)






@app.route('/', methods=['GET'])
def testeur():
    return "hohoho"

"""
@app.route('/verifyimage/<string:image_reference>', methods=['GET'])
def verifyimage(image_reference):
    ut = Utilisateur.query.filter(Utilisateur.image_reference.like("%"+image_reference+"%"))

    if len(ut)==0:
        return 0
    else:
        return ut.id

@app.route('/verifyrfid/<string:rfid_reference>', methods=['GET'])
def verifyrfid(rfid_reference):
    ut = Utilisateur.query.filter(Utilisateur.rfid_reference.like("%"+rfid_reference+"%"))

    if len(ut)==0:
        return 0
    else:
        return ut.id

@app.route('/verifyqr/<string:qr_reference>', methods=['GET'])
def verifyqr(qr_reference):
    ut = Utilisateur.query.filter(Utilisateur.qr_reference.like("%"+qr_reference+"%"))

    if len(ut)==0:
        return 0
    else:
        return ut.id
   

@app.route('/users', methods=['GET'])
def users():
    req_info = Utilisateur.query.all()
    info = json.loads(req_info.decode('utf-8'))
    


    return jsonify(
    status=200,
    content=info
    )






#db.create_all()
"""



if __name__ == '__main__':
    db.create_all()
    app.run(debug=False)




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
    name=db.Column(db.String(60))
    image_reference=db.Column(db.String(60))
    qr_reference = db.Column(db.String(128))
    rfid_reference=db.Column(db.String(60))
 


    def __repr__(self):
        return '<utilisateur: {}>'.format(self.id)

class Historique(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    action =db.Column(db.String(80))
    date=db.Column(db.DateTime)
    utilisateur=db.Column(db.Integer)
    loginmode=db.Column(db.String(80))

    def __repr__(self):
        return '<utilisateur: {}>'.format(self.id)






@app.route('/', methods=['GET'])
def testeur():
    return "Hello this is your fav API "



#this path allow you to have all the users
@app.route('/users', methods=['GET'])
def users():
    
    users=Utilisateur.query.all()
    data=[]

    for user in users:
        data.append({"id":user.id,"name":user.name,"image_reference":user.image_reference,"rfid_reference":user.rfid_reference,"qr_reference":user.qr_reference})
    return jsonify(
    status=200,
    content=data
    )


    



#this path allow you to add an user
@app.route('/adduser', methods=['POST'])
def adduser():

    try:           
        data = request.get_json()
        print(data)
        userToAdd= Utilisateur(name=data['name'],image_reference=data['image_reference'],qr_reference=data['qr_reference'],rfid_reference=data['rfid_reference']) 
        db.session.add(userToAdd)
        db.session.commit()
        return "yes"
    except ValueError:
        return "no"

#this path allow you to have all the histique's log
@app.route('/historiques',methods=['GET'])
def historiques():
    historiques=Historique.query.all()
    data=[]
    for historique in historiques:
        data.append({"id":historique.id,"loginmode":historique.loginmode,"utilisateur":historique.utilisateur,"date":historique.date})
   

    return jsonify(
    status=200,
    content=data
    )



#this function allow you to add a historique's log
def addhistorique(idUser,loginmode,action):
    try:
            
        historiqueToAdd= Historique(action=action,utilisateur=idUser,loginmode=loginmode,date=datetime.now()) 
        db.session.add(historiqueToAdd)
        db.session.commit()
        return "yes"
    except :
        return "no"



#this path allow an user to try to authentificate with image
@app.route('/verifyimage/<string:image_reference>', methods=['GET'])
def verifyimage(image_reference):
    ut = Utilisateur.query.filter_by(image_reference=image_reference).first()

    try:
        addhistorique(ut.id,"IMAGE","pointage")
    except :
        return "no"
        
    return "yes"


#this path allow an user to try to authentificate with rfid tag
@app.route('/verifyrfid/<string:rfid>', methods=['GET'])
def verifyrfid(rfid):
    ut = Utilisateur.query.filter_by(rfid_reference=rfid).first()

    try:
        addhistorique(ut.id,"RFID","pointage")
    except :
        return "no"
    


    return "yes"

#this path allow an user to try to authentificate with qrcode
@app.route('/verifyqr/<string:qr_reference>', methods=['GET'])
def verifyqr(qr_reference):
    ut = Utilisateur.query.filter_by(qr_reference=qr_reference).first()

    try:
        addhistorique(ut.id,"QR_CODE","pointage")
    except :
        return "no"
    


    return "yes"




#db.create_all()




if __name__ == '__main__':
    db.create_all()
    app.run(debug=False)




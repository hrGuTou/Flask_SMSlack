import json
from flask_sqlalchemy import SQLAlchemy

from flask import Flask, request, jsonify, url_for
from sqlalchemy import Column, Integer, String
from twilio.twiml.messaging_response import MessagingResponse
from werkzeug.utils import redirect

from parser import *
from database import *
import control
import bcrypt
from flask_cors import CORS
from flask_login import LoginManager, current_user, login_user, UserMixin, login_required, logout_user

cur = db.cursor()



def startApp():
    app = Flask(__name__)



    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqldb://GuTou:GuTou@localhost:3306/on9db'
    app.config['SECRET_KEY'] = "this"
    CORS(app)
    db = SQLAlchemy(app)
    login_manager = LoginManager()
    login_manager.init_app(app)

    class User(UserMixin, db.Model):
        id = Column("id", Integer, primary_key=True, autoincrement=True)
        username = Column("Email", String, unique=True)
        password = Column("Password", String)

    @app.route('/sms', methods=['POST'])
    def sms():
        num = request.form['From']

        msg = request.form['Body']
        response = MessagingResponse()

        if num not in listofNum:
            res = control.greeting(response, 'CS336')
            listofNum.append(num)
            return res
        else:
            if msg.rfind("[INFO]") != -1:
                infoParser(msg, num)
            return "OK"

    @app.route('/api/participants')
    def listallparticipant():
        data = control.listAllParticipant()
        result = {}
        for row in data:
            result.update({
                row[2]: {
                    'Name': row[0],
                    'Email': row[1],
                    'Phone Number': row[2],
                    'Sex': row[3],
                    'Team Name': row[4],
                    'Project Name': row[5]
                }})

        res = jsonify(result)
        res.status_code = 200
        return res

    @app.route('/api/names')
    def name():
        data = control.names()
        res = jsonify(data)
        res.status_code = 200
        return res

    @app.route('/api/teams')
    def teams():
        data = control.teams()
        res = jsonify(data)
        res.status_code=200
        return res

    @app.route('/api/announcement_history')
    def amHistory():
        data = control.amHistory()
        res = {}
        for list in data:
            res.update({
                list[0]:list[1]
            })

        res = jsonify(res)
        res.status_code=200
        return res

    @app.route('/api/group_history')
    def gmHistory():
        data = control.gmHistory()
        res = {}
        for list in data:
            res.update({
                list[1]:{
                    'Team Name':list[0],
                    'Message':list[2]
                }
            })

        res = jsonify(res)
        res.status_code=200
        return res

    @app.route('/api/personal_history')
    def pmHistory():
        data = control.pmHistory()
        res = {}
        for list in data:
            res.update({
                list[1]:{
                    'Name':list[0],
                    'Message':list[2]
                }
            })

        res = jsonify(res)
        res.status_code=200
        return res

    @app.route('/api/send_announce', methods = ['POST'])
    def sendAM():
        """
            request: POST
            data type: JSON
            {
                'Message':messageData
            }

        :return:
        """
        data = request.json
        control.sendAnnouncement(data['Message'])
        return json.dumps(request.json)

    @app.route('/api/send_group', methods = ['POST'])
    def sendGM():
        """
            request: POST
            data type: JSON
            {
               'Message':messageData,
               'Team Name':teamName,
            }

            :return:
        """
        data = request.json
        control.sendGM(data['Message'],data['Team Name'])
        return json.dumps(request.json)

    @app.route('/api/send_person', methods=['POST'])
    def sendPM():
        """
            request: POST
            data type: JSON
            {
               'Message':messageData,
               'Name':listOfName
            }

            :return:
        """
        data = request.json
        control.sendPM(data['Message'], data['Name'])
        return json.dumps(request.json)

    @app.route('/api/signup', methods = ['POST'])
    def signup():
        data = request.json
        usr = data['email']
        psd = data['password']
        hashedPSD = bcrypt.hashpw(psd.encode("utf8"), bcrypt.gensalt())

        control.signup(usr,hashedPSD)

        print(data)
        return json.dumps(request.json)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))


    @app.route('/api/login', methods= ['GET','POST'])
    def login():
        data = request.json
        email = data['email']
        psd = data['password']
        usr = User.query.filter_by(username=email).first()

        if usr.password is not None and bcrypt.checkpw(psd.encode('utf8'),usr.password.encode('utf8')):
            login_user(usr)
            print("login")
            return redirect(url_for('signup'),code=302)
        else:
            print("bad")
            return "BAD LOGIN"

    @app.route('/api/logout')
    @login_required
    def logout():
        logout_user()
        return 'logout'

    makeTable()
    app.run()



listofNum = []

if __name__ == '__main__':
    #    listofNum = []
    #    eventName = input("Event Name: ")
    #    app = startApp(eventName)
    #    makeTable()
    #    app.run()
    startApp()

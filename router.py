import json

from flask import Flask, request, jsonify
from twilio.twiml.messaging_response import MessagingResponse
from parser import *
from database import *
import control

cur = db.cursor()


def infoParser(info, num):
    result = dataParser(info)
    dataRec = {'Name': result[0],
               'Email': result[1],
               'Sex': result[2],
               'Team Name': result[3],
               'Project Name': result[4],
               'Project Status': result[5],
               'PhoneNumber': num}
    print(dataRec)  # for debug
    insINFO(dataRec)


def greeting(res, eventName):
    res.message("Welcome to " + eventName + "! Please copy&paste the following message to fill in and reply. "
                                            "(KEEP EXACT FORMAT)")
    res.message("[INFO]\n"
                "Name(first last):\n"
                "Email:\n"
                "Sex(M/F):\n"
                "Team Name:\n"
                "Project Name:\n"
                "Project status(C for complete,I for incomplete):")
    return str(res)


def startApp():
    app = Flask(__name__)

    @app.route('/sms', methods=['POST'])
    def sms():
        num = request.form['From']

        msg = request.form['Body']
        response = MessagingResponse()

        if num not in listofNum:
            res = greeting(response, 'CS336')
            listofNum.append(num)
            return res
        else:
            if msg.rfind("[INFO]") != -1:
                infoParser(msg, num)
            return "OK"

    @app.route('/participants')
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

    @app.route('/names')
    def name():
        data = control.names()
        res = jsonify(data)
        res.status_code = 200
        return res

    @app.route('/teams')
    def teams():
        data = control.teams()
        res = jsonify(data)
        res.status_code=200
        return res

    @app.route('/announcement_history')
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

    @app.route('/group_history')
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

    @app.route('/personal_history')
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

    @app.route('/send_announce', methods = ['POST'])
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

    @app.route('/send_group', methods = ['POST'])
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
        control.sendGM(data['Message'],['Team Name'])
        return json.dumps(request.json)

    @app.route('/send_person', methods=['POST'])
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
        control.sendPM(data['Message'], ['Name'])
        return json.dumps(request.json)




    app.run()


listofNum = []

if __name__ == '__main__':
    #    listofNum = []
    #    eventName = input("Event Name: ")
    #    app = startApp(eventName)
    #    makeTable()
    #    app.run()
    startApp()

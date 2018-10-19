from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from Parser import *
from database import *


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
                                            "(Keep exact format)")
    res.message("[INFO]\n"
                "Name(first last):\n"
                "Email:\n"
                "Sex(M/F):\n"
                "Team Name:\n"
                "Project Name:\n"
                "Project status(C for complete,I for incomplete):")
    return str(res)


def startApp(eventName):
    app = Flask(__name__)

    @app.route('/sms', methods=['POST'])
    def sms():
        num = request.form['From']

        msg = request.form['Body']
        response = MessagingResponse()

        if num not in listofNum:
            res = greeting(response, eventName)
            listofNum.append(num)
            return res
        else:
            if msg.rfind("[INFO]") != -1:
                infoParser(msg, num)
            return "OK"

    return app


# if __name__ == '__main__':
listofNum = []
# eventName = input("Event Name: ")
# app = startApp()
# makeTable()
# app.run()

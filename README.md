# SMslack
This project used MYSQL database and Twilio sms API to build a web platform mainly for event organizers to send out notifications and announcements via SMS.

# Environment Setup
Install MYSQL for database management.<br />
Have Twilio account ready.<br />
Install ngrok or alternative services to expose localhost.<br />
<br />
For ngrok, use the following command in terminal to start:<br />
`$ ngrok http FLASK_RUNNING_PORT -host-header="localhost:FLASK_RUNNING_PORT"`<br />
Copy generated http link and paste it into your Twilio SMS webhook.<br />

# Usage
Enter Twilio api (account_sid and token) information and Twilio phone number in `control.py`<br />
Fill in database information.<br />
Start backend at `router.py`<br />

All control functions located in `control.py`. Modify if needed.<br />

# Database Tables
1.Announcement<br />
2.GroupMsg<br />
3.Participant<br />
4.PrivateMsg<br />
5.Project<br />
6.Team<br />

# TODO
1.Fix possible bugs and check inputs<br />
2.Front end implementation<br />

# Group Members
Haoran He<br />
Kai Hang Chen<br />

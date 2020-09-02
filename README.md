# pyportfo
My python learning [portfolio](http://sunflail.pythonanywhere.com).

Server.py contains the flask code.<br><br>
API keys for sendgrid need to be stored in local/hosted .env with appropriate keys.<br><br>
Included is a commented out section to utilize SMTP instead of the sendgrid API, however
this requires a paid PythonAnywhere account or to be hosted on a site that allows smtp traffic.<br><br>
Contact page email form will save information to database.txt, database.csv, and email using either SMTP or
SendGrid's API depending on what you choose. Make sure to include database.* in your .gitignore once you start
using the form for live data.<br><br>
HTML/CSS/JS template pulled from Mashup, and initial project was done through the ZeroToMaster.io Python course.<br><br>


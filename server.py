from flask import Flask, render_template, request, redirect
import csv
import os
# from dotenv import load_dotenv

# project_folder = os.path.expanduser('./')
# load_dotenv(os.path.join(project_folder, '.env'))
app = Flask(__name__)
# app.config.from_pyfile('config.py')

@app.route('/')
def root():
    return render_template('index.html')

@app.route('/<string:page_name>')
def html_page(page_name):
    return render_template(page_name)

def write_to_file(data):
    with open('database.txt' , mode='a') as database:
        email = data["email"]
        subject = data["subject"]
        message = data["message"]
        database.write(f'\n{email},{subject},\n{message}')

'''This correctly sends an email but requires gmail to have less secure apps allowed. Sendgrid working with smtp
on a local instance, but pythonanywhere only has api.sendgrid.com in the whitelist for free account, so need to change
to the api to use as production.
import smtplib
from email.message import EmailMessage
def send_email(data):
    email = EmailMessage()
    # email['from'] = data["email"]
    email['from'] = os.getenv("SGVerifiedSender")
    email['to'] = os.getenv("SGVerifiedSender")
    email['subject'] = data["subject"]
    email.set_content(f' From: {data["email"]}\n {data["message"]}')
    SendGridKey = os.getenv("SendGridKey")
    # GmailKey = os.getenv("GmailKey")
    with smtplib.SMTP_SSL(host='smtp.sendgrid.net', port=465) as smtp:
        try:
            smtp.ehlo()
            smtp.starttls()
        except:
            print("no tls")
        try:
            smtp.login('apikey', SendGridKey)
        except:
            print("login error")
        # smtp.set_debuglevel(3)
        smtp.send_message(email)
        smtp.quit()
'''

#Use this section for the sendgrid v3 api
import sendgrid
from sendgrid.helpers.mail import *
def send_email(data):
    sg = sendgrid.SendGridAPIClient(api_key=os.environ.get('SendGridKey'))
    from_email = Email(os.getenv("SGVerifiedSender")) #has to come from verified sender
    to_email = To(os.getenv("SGVerifiedSender"))
    subject = data["subject"]
    content = Content("text/plain", f'From: {(data["email"])}\n {data["message"]}')
    mail = Mail(from_email,to_email,subject,content)
    response = sg.client.mail.send.post(request_body=mail.get())
    print(response.status_code)
    print(response.body)
    print(response.headers)

def write_to_csv(data):
    with open('database.csv' , mode='a', newline='') as database2:
        email = data["email"]
        subject = data["subject"]
        message = data["message"]
        csv_writer = csv.writer(database2, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        csv_writer.writerow([email,subject,message])

@app.route('/submit_form', methods=['POST', 'GET'])
def submit_form():
    if request.method == 'POST':
        try:
            data = request.form.to_dict()
            write_to_file(data)
        except:
            return 'database.txt not written to'
        try:
            data = request.form.to_dict()
            write_to_csv(data)
        except:
            return 'database.csv not written to'
        try:
            data = request.form.to_dict()
            print(data)
            send_email(data) #this is causing a type error, sometimes timeout error - works fine not in a function
            return redirect('/thankyou.html')
        except smtplib.SMTPHeloError:
            print('helo error')
        except smtplib.SMTPRecipientsRefused:
            print('recipient error')
        except smtplib.SMTPSenderRefused:
            print('recipient error')
        except smtplib.SMTPDataError:
            print('recipient error')
        except (smtplib.SMTPAuthenticationError, smtplib.SMTPConnectError, smtplib.SMTPNotSupportedError, smtplib.SMTPServerDisconnected, smtplib.SMTPDataError):
            print('recipient error')
    else:
        return 'something went wrong, method not POST, try again'


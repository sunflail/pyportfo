import os
from dotenv import load_dotenv

project_folder = os.path.expanduser('./')
load_dotenv(os.path.join(project_folder, '.env'))

TESTING = True
DEBUG = True
FLASK_ENV = 'development'
SendGridKey = os.getenv("SendGridKey")
GmailKey = os.getenv("GmailKey")

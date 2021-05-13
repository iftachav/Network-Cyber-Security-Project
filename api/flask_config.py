import os
from flask import Flask
from flask_cors import CORS
from flask_mail import Mail

app = Flask(__name__)

app.config["MAIL_SERVER"] = 'smtp.gmail.com'
app.config["MAIL_PORT"] = 587  # or 465
app.config["MAIL_USE_TLS"] = True
app.config["MAIL_USE_SSL"] = False
app.config["MAIL_USERNAME"] = os.environ.get("MAIL_USERNAME")
app.config["MAIL_PASSWORD"] = os.environ.get("MAIL_PASSWORD")

CORS(app)
cors = CORS(app, resources={
    r"/*":{
        "origins":"*"
    }
})
mail = Mail(app)

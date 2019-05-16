from datetime import datetime
from flask import Flask, render_template, request, url_for, redirect
from werkzeug.utils import secure_filename
from flask_sqlalchemy import SQLAlchemy

####################### SETTING ########################

UPLOAD_FOLDER = 'static/images/meals'
ALLOWED_EXTENSIONS = (['pdf', 'png', 'jpg', 'jpeg', 'gif'])

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///d_m.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
db = SQLAlchemy(app)


###########################################################################

############################## MODELS #####################################
class Meals(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), nullable=False)
    inf = db.Column(db.Text)
    price = db.Column(db.Numeric(10, 2))
    requests = db.relationship('Requests', backref='meal')
    photo_id = db.Column(db.Integer, db.ForeignKey('photos.id'))


class Requests(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name_user = db.Column(db.String(50), nullable=False)
    address = db.Column(db.Text, nullable=False )
    date_time = db.Column(db.DateTime(timezone=True), default=datetime.now())
    meal_id = db.Column(db.Integer, db.ForeignKey('Meals.id'))


class Photos(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    url = db.Column(db.Text, nullable=False)
    meals = db.relationship('Meals', backref='photo')
##############################################################################




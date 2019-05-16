from datetime import datetime
from random import randrange
from os import path, listdir, remove
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
    address = db.Column(db.Text, nullable=False)
    is_active = db.Column(db.Boolean, default=False)
    request_date = db.Column(db.DateTime(timezone=True), default=datetime.now())
    delivery_date = db.Column(db.DateTime(timezone=True), onupdate=datetime.now())
    meal_id = db.Column(db.Integer, db.ForeignKey('Meals.id'))


class Photos(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    url = db.Column(db.Text, nullable=False)
    meals = db.relationship('Meals', backref='photo')


db.create_all()


class operations:
    # This operations which control the tables

    # Meals
    def add_meal(self, name, inf='', price=None, photo_id=None):
        meal = Meals(name=name, inf=inf, price=price, photo_id=photo_id)
        db.session.add(meal)
        db.session.commit()
        return meal.id

    def get_meal_by_id(self, id):
        return Meals.query.get(id)

    def get_all_meal(self):
        return Meals.query.all()

    def get_meal_by_name(self, name):
        return Meals.query.filter(Meals.name == name).first()

    def update_meal(self, id, name, inf, price):
        meal = self.get_meal_by_id(id)
        meal.name = name
        meal.inf = inf
        meal.price = price
        db.session.commit()

    # Requests
    def add_request(self, name_user, address, meal):
        db.session.add(Requests(name_user=name_user, address=address, meal_id=meal))
        db.session.commit()

    def get_request_by_id(self, id):
        return Requests.query.get(id)

    def get_all_requests(self):
        x = Requests.query.order_by(Requests.date_time.desc()).all()
        return x

    def request_ok(self, id):
        requests = self.get_request_by_id(id)
        requests.is_active = True
        db.session.commit()

    # PHOTOS
    def add_photo(self, url):
        photo = Photos(url=url)
        db.session.add(photo)
        db.session.commit()
        return photo.id

    def get_url_photo_by_id(self, id):
        photo = Photos.query.get(id)
        return photo.url

    def update_photo(self, id, url):
        photo = Photos.query.get(id)
        photo.url = url
        db.session.commit()


######################################################################################

o = operations()


################################# FUNCTIONS ############################################
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'photo_url' not in request.files:
            return redirect(request.url)
        file = request.files['photo_url']
        # if user does not select file, browser also
        # submit a empty part without filename
        name_file = file.filename
        if name_file == '':
            return ''
        if file.filename in listdir(UPLOAD_FOLDER):
            z = randrange(10000)
            name_file = str(z) + file.filename
        if file and allowed_file(file.filename):
            file.filename = name_file
            name_file = secure_filename(file.filename)
            file.save(path.join(app.config['UPLOAD_FOLDER'], name_file))
            return app.config['UPLOAD_FOLDER'] + '/' + name_file
#########################################################################

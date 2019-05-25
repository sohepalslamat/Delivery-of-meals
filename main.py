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
    desc = db.Column(db.Text)
    price = db.Column(db.Numeric(10, 2))
    requests = db.relationship('Requests', backref='meal')
    photo_id = db.Column(db.Integer, db.ForeignKey('photos.id'))


class Requests(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name_user = db.Column(db.String(50), nullable=False)
    address = db.Column(db.Text, nullable=False)
    is_active = db.Column(db.Boolean, default=False)
    amount = db.Column(db.Integer, default=1)
    request_date = db.Column(db.DateTime(timezone=True), default=datetime.now())
    delivery_date = db.Column(db.DateTime(timezone=True), onupdate=datetime.now())
    meal_id = db.Column(db.Integer, db.ForeignKey('meals.id'))


class Photos(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    url = db.Column(db.Text, nullable=False)
    meals = db.relationship('Meals', backref='photo')


db.create_all()


class operations:
    # This operations which control the tables

    # Meals
    def add_meal(self, name, desc='', price=None, photo_id=None):
        meal = Meals(name=name, desc=desc, price=price, photo_id=photo_id)
        db.session.add(meal)
        db.session.commit()
        return meal.id

    def get_meal_by_id(self, id):
        return Meals.query.get(id)

    def get_all_meal(self):
        return Meals.query.all()

    def get_meal_by_name(self, name):
        return Meals.query.filter(Meals.name == name).first()

    def update_meal(self, id, name, desc, price):
        meal = self.get_meal_by_id(id)
        meal.name = name
        meal.desc = desc
        meal.price = price
        db.session.commit()

    def delete_meal(self, id):
        Meals.query.filter_by(id=id).delete()
        db.session.commit()

    # Requests
    def add_request(self, name_user, address, meal):
        db.session.add(Requests(name_user=name_user, address=address, meal_id=meal))
        db.session.commit()

    def get_request_by_id(self, id):
        return Requests.query.get(id)

    def get_all_requests_by_date(self):
        x = Requests.query.order_by(Requests.request_date.desc()).all()
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
        if 'mealImage' not in request.files:
            return redirect(request.url)
        file = request.files['mealImage']
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
            return '/' + app.config['UPLOAD_FOLDER'] + '/' + name_file


#########################################################################


############################# VIEWS #####################################

@app.route('/')
def homepage():
    return render_template('homepage.html')


######### Admin ##########

@app.route('/admin')
def admin():
    return render_template('admin-dashboard.html')


@app.route('/admin/meals')
def show_meals_for_admin():
    meals = o.get_all_meal()
    return render_template('show-meals-for-admin.html', meals=meals)


@app.route('/admin/meals/add_meal', methods=['POST', 'GET'])
def add_meal():
    if request.method == 'POST':
        try:
            url_photo = upload_file()
            photo_id = o.add_photo(url=url_photo)
            o.add_meal(name=request.form['mealName'], desc=request.form['mealDesc'],
                       price=request.form['price'], photo_id=photo_id)
            return redirect(url_for('show_meals_for_admin'))
        except:
            return redirect(request.url)
    elif request.method == 'GET':
        return render_template('add-meal.html')


@app.route('/admin/meals/update/<int:id>', methods=['GET', 'POST'])
def update_meal(id):
    if request.method == 'POST':
        try:
            url_photo = upload_file()
            if url_photo != '':
                meal = o.get_meal_by_id(id)
                photo_id = meal.photo.id
                last_url = o.get_url_photo_by_id(photo_id)
                if path.exists(last_url):
                    remove(last_url)
                o.update_photo(id=photo_id, url=url_photo)
            o.update_meal(id=id, name=request.form['mealName'], desc=request.form['mealDesc'],
                          price=request.form['price'])
            return redirect(url_for('show_meals_for_admin'))
        except:
            return redirect(request.url)
    elif request.method == 'GET':
        context = o.get_meal_by_id(id)
        return render_template('update-meal.html', meal=context)


@app.route('/admin/meals/delete/<int:id>')
def delete_meal(id):
    meal = o.get_meal_by_id(id)
    photo_id = meal.photo.id
    photo_url = o.get_url_photo_by_id(photo_id)
    if path.exists(photo_url):
        remove(photo_url)
    o.delete_meal(id)
    return redirect(url_for('show_meals_for_admin'))


@app.route('/admin/requests', methods=['GET', 'POST'])
def requests():
    if request.method == 'POST':
        '''
        requests = o.get_all_requests_by_date()
        for i in requests:
            x = request.form['checkbox-status-form-'+str(i.id)]
            print(x)
            if x == 'True':
                o.request_ok(i.id)
        '''

        return redirect(url_for('requests'))

    elif request.method == 'GET':
        requests = o.get_all_requests_by_date()
        return render_template('show-request-for-admin.html', requests=requests)


#############ُ End Admin ###############


#############################################################################
app.run()

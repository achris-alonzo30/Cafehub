import base64
from flask import Flask, render_template, request, redirect, url_for
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TimeField, SelectField, BooleanField
from wtforms.validators import DataRequired, URL

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cafes_database.db'  # Change the URI according to your database setup
db = SQLAlchemy(app)
Bootstrap(app)


# ----------------------------------------- Create a model for the database --------------------------------------- #
class Cafe(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    image = db.Column(db.LargeBinary, nullable = True)
    cafe_name = db.Column(db.String(100), nullable = False)
    location = db.Column(db.String(200), nullable = False)
    website_url = db.Column(db.String(200), nullable = False)
    open_time = db.Column(db.Time, nullable = False)
    closing_time = db.Column(db.Time, nullable = False)
    open_time_saturday = db.Column(db.Time, nullable = True)
    closing_time_saturday = db.Column(db.Time, nullable = True)
    open_time_sunday = db.Column(db.Time, nullable = True)
    closing_time_sunday = db.Column(db.Time, nullable = True)
    coffee_rating = db.Column(db.String(1), nullable = False)
    food_rating = db.Column(db.String(1), nullable = False)
    wifi_rating = db.Column(db.String(1), nullable = False)
    power_outlet_rating = db.Column(db.String(1), nullable = False)
    tier_prices = db.Column(db.String(1), nullable = False)
    number_of_tables = db.Column(db.String(1), nullable = False)
    the_vibe = db.Column(db.String(100), nullable = False)
    quietness = db.Column(db.String(100), nullable = False)
    restroom = db.Column(db.String(100), nullable = False)


# ---------------------------------------------- List of image paths ---------------------------------------- #
carousel_images = [
    "static/images/1.png",
    "static/images/2.png",
    "static/images/3.png",
    "static/images/4.png",
    "static/images/5.png",
    "static/images/6.png",
    "static/images/7.png",
]


# -------------------------------------------------- Flask Forms --------------------------------------------------#
class CafeForm(FlaskForm):
    # Basic Information
    cafe = StringField('Cafe Name', validators = [DataRequired()])
    location = StringField('Cafe Location on Google Maps(URL)', validators = [DataRequired(), URL()])
    website_url = StringField('Cafe Website URL', validators = [DataRequired(), URL()])
    open_time = TimeField('Opening Time', validators = [DataRequired()])
    closing_time = TimeField('Closing Time', validators = [DataRequired()])
    open_time_saturday = TimeField('Saturday Opening Time', validators = [DataRequired()])
    closing_time_saturday = TimeField('Saturday Closing Time', validators = [DataRequired()])
    open_time_sunday = TimeField('Sunday Opening Time', validators = [DataRequired()])
    closing_time_sunday = TimeField('Sunday Closing Time', validators = [DataRequired()])

    # Ratings
    coffee_rating = SelectField('Coffee Rating', choices = [
        ('1', '☕️'),
        ('2', '☕️☕️'),
        ('3', '☕️☕️☕️'),
        ('4', '☕️☕️☕️☕️'),
        ('5', '☕️☕️☕️☕️☕️')],
                                validators = [DataRequired()])

    food_rating = SelectField('Food Rating', choices = [
        ('1', '🥯'),
        ('2', '🥯🥯'),
        ('3', '🥯🥯🥯'),
        ('4', '🥯🥯🥯🥯'),
        ('5', '🥯🥯🥯🥯🥯')],
                              validators = [DataRequired()])

    wifi_rating = SelectField('WiFi Rating', choices = [
        ('0', '✘'),
        ('1', '🛜'),
        ('2', '🛜🛜'),
        ('3', '🛜🛜🛜'),
        ('4', '🛜🛜🛜🛜'),
        ('5', '🛜🛜🛜🛜🛜')],
                              validators = [DataRequired()])

    power_outlet_rating = SelectField('Power Outlet Rating', choices = [
        ('0', '✘'),
        ('1', '🔌'),
        ('2', '🔌🔌'),
        ('3', '🔌🔌🔌'),
        ('4', '🔌🔌🔌🔌'),
        ('5', '🔌🔌🔌🔌🔌')],
                                      validators = [DataRequired()])

    # Cafe Features
    tier_prices = SelectField('How expensive?', choices = [
        ('1', '💸'),  # Low price
        ('2', '💸💸'),  # Moderate price
        ('3', '💸💸💸'),  # Higher price
        ('4', '💸💸💸💸')],  # Expensive price
                              validators = [DataRequired()])

    number_of_tables = SelectField('Number of Tables', choices = [
        ('1', '0-10'),
        ('2', '10-30'),
        ('3', '30+')],
                                   validators = [DataRequired()])

    the_vibe = SelectField('The Vibe', choices = [
        ('Cozy', 'Cozy and Comfortable'),  # Cozy and Comfortable setting
        ('Lively', 'Lively and Energetic'),  # Lively and Energetic vibe
        ('Productive', 'Productive and Inspiring'),  # Productive and Inspiring atmosphere
        ('Chill', 'Chill and Relaxed'),  # Chill and Relaxed ambiance
        ('Social', 'Social and Friendly'),  # Social and Friendly environment
        ('Studious', 'Studious and Academic'),  # Studious and Academic atmosphere
        ('Modern', 'Modern and Trendy'),  # Modern and Trendy setting
        ('Rustic', 'Rustic and Vintage'),  # Rustic and Vintage vibe
        ('Artistic', 'Artistic and Creative'),  # Artistic and Creative ambiance
        ('Uncomfortable', 'Uncomfortable'),  # Uncomfortable and Awkward setting
        ('Unfriendly', 'Unfriendly and Unwelcoming'),  # Unfriendly and Unwelcoming vibe
        ('Distracting', 'Distracting and Disruptive'),  # Distracting and Disruptive ambiance
        ('Outdated', 'Outdated and Run-down')],  # Outdated and Run-down atmosphere
                           validators = [DataRequired()])

    quietness = SelectField('Quietness', choices = [
        ('Quiet', 'Quiet and Peaceful'),  # Quiet and Peaceful atmosphere
        ('Chaotic', 'Chaotic and Noisy')],  # Chaotic and Noisy atmosphere
                            validators = [DataRequired()])

    restroom = SelectField('Restroom', choices = [
        ('Clean', 'Clean and Comfortable'),  # Clean and Comfortable restroom
        ('Dirty', 'Dirty and Unpleasant')],  # Dirty and Unpleasant restroom
                           validators = [DataRequired()])

    submit = SubmitField('Submit')


class JoinForm(FlaskForm):
    fname = StringField('First Name', validators = [DataRequired()])
    lname = StringField('Last Name', validators = [DataRequired()])
    email = StringField('Email', validators = [DataRequired()])
    favourite_location = StringField('Share your favourite location. (Optional)', validators = [URL()])
    submit = SubmitField('Submit')


def calculate_total_rating(coffee_rating, food_rating, wifi_rating, power_outlet_rating):
    # Convert arguments to integers
    coffee_rating = int(coffee_rating)
    food_rating = int(food_rating)
    wifi_rating = int(wifi_rating)
    power_outlet_rating = int(power_outlet_rating)

    # Your calculation logic here
    total_rating = coffee_rating + food_rating + wifi_rating + power_outlet_rating
    percentage = round((total_rating / 20) * 100, 2)

    return percentage


def format_time(time_obj):
    if time_obj is None:
        return ""
    formatted_time = time_obj.strftime("%I:%M %p")
    return formatted_time


# -------------------------------------------------- Flask Routes --------------------------------------------------#
@app.route("/")
def home():
    return render_template("index.html", carousel_images = carousel_images)


@app.route('/cafes', methods=['GET'])
def cafes():
    # Retrieve cafés from the database
    cafes_list = Cafe.query.all()

    # Calculate the total rating for each café
    for cafe in cafes_list:
        cafe.total_rating = calculate_total_rating(cafe.coffee_rating,
                                                   cafe.food_rating,
                                                   cafe.wifi_rating,
                                                   cafe.power_outlet_rating)

    return render_template('cafes.html', cafes=cafes_list)


@app.route('/add-cafes', methods = ['GET', 'POST'])
def add_cafes():
    form = CafeForm()

    if form.validate_on_submit():

        # Create a new Café object with the form data
        new_cafe = Cafe(
            cafe_name = form.cafe.data.title(),
            location = form.location.data,
            website_url = form.website_url.data,
            open_time = form.open_time.data,
            closing_time = form.closing_time.data,
            coffee_rating = form.coffee_rating.data,
            food_rating = form.food_rating.data,
            wifi_rating = form.wifi_rating.data,
            power_outlet_rating = form.power_outlet_rating.data,
            tier_prices = form.tier_prices.data,
            number_of_tables = form.number_of_tables.data,
            the_vibe = form.the_vibe.data,
            quietness = form.quietness.data,
            restroom = form.restroom.data,
        )

        if 'cafe_image' in request.files:
            file = request.files['cafe_image']
            print("File:", file)
            if file and file.filename != '':
                # Read the image file data as bytes
                image_data = file.read()
                print("Image Data:", image_data)

                # Get the image format from the filename or content type
                image_format = file.filename.split('.')[-1].lower()
                print("Image Format:", image_format)

                # Save the image data and format to the new_cafe object
                new_cafe.image = image_data
                new_cafe.image_format = image_format

        # Save the new café object to the database
        db.session.add(new_cafe)
        db.session.commit()

        # Redirect to the café page to display the message
        return redirect(url_for('cafes'))

    # If a form submission fails, or it's a GET request, render the add_cafes.html template with the form
    return render_template('add_cafes.html', form = form)


@app.route('/join-us', methods = ['GET', 'POST'])
def join():
    form = JoinForm()

    return render_template('join.html', form = form)


# Custom filter or templates
@app.template_filter('b64encode')  # Convert binary data to base64 string
def base64_encode(data):
    return base64.b64encode(data).decode('utf-8')


# Add the format_time function to Jinja's environment
app.jinja_env.filters['format_time'] = format_time

if __name__ == '__main__':

    app.run(debug = True)

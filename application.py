from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from flask_cors import CORS
from flask_migrate import Migrate
from werkzeug.security import generate_password_hash, check_password_hash
from flask_mail import Mail, Message
import pickle
import pandas as pd
import numpy as np
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
cors = CORS(app)

model = pickle.load(open('LinearRegressionModel.pkl', 'rb'))
car = pd.read_csv('Cleaned_Car_data.csv')

migrate = Migrate(app, db)

app.config['MAIL_SERVER'] = 'smtp.gmail.com'  # For Gmail
app.config['MAIL_PORT'] = 465  # For Gmail SSL
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = 'your_email@gmail.com'  # Replace with your email when running locally
app.config['MAIL_PASSWORD'] = 'your_app_password_here'  # Replace with your app password when running locally
app.config['MAIL_DEFAULT_SENDER'] = 'your_email@gmail.com'  # Replace with your email when running locally

mail = Mail(app)


# User model
# # Add the Prediction model
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False, unique=True)
    email = db.Column(db.String(120), nullable=False, unique=True)
    password = db.Column(db.String(200), nullable=False)
    # No need to define a 'predictions' property manually
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

# Prediction model
class Prediction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    company = db.Column(db.String(100), nullable=False)
    car_model = db.Column(db.String(100), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    fuel_type = db.Column(db.String(50), nullable=False)
    kilometers_driven = db.Column(db.Integer, nullable=False)
    predicted_price = db.Column(db.Float, nullable=False)

    # Define a backref with a unique name
    user = db.relationship('User', backref=db.backref('user_predictions', lazy=True))


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
def home():
    if current_user.is_authenticated:
        # Render index.html (dashboard) if the user is logged in
        companies = sorted(car['company'].unique())
        car_models = sorted(car['name'].unique())
        year = sorted(car['year'].unique(), reverse=True)
        fuel_type = car['fuel_type'].unique()

        companies.insert(0, 'Select Company')
        return render_template('index.html', companies=companies, car_models=car_models, years=year, fuel_types=fuel_type)
    
    # If not logged in, render the landing page
    return render_template('landing_page.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        new_user = User(username=username, email=email, password=hashed_password)

        try:
            db.session.add(new_user)
            db.session.commit()
            flash('Signup successful. Please log in.', 'success')
            return redirect(url_for('login'))
        except:
            flash('User with this email or username already exists.', 'danger')

    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()

        if user and bcrypt.check_password_hash(user.password, password):
            login_user(user)
            flash('Login successful!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid email or password.', 'danger')

    return render_template('login.html')

@app.route('/profile')
@login_required
def profile():
    # Get the user's personal information
    user_info = {
        'username': current_user.username,
        'email': current_user.email
    }

    # Fetch the user's prediction history
    predictions = Prediction.query.filter_by(user_id=current_user.id).all()

    # Pass both user info and predictions to the template
    return render_template('profile.html', user_info=user_info, predictions=predictions)

@app.route('/send_email/<int:prediction_id>', methods=['GET'])
@login_required
def send_email(prediction_id):
    # Fetch the prediction details
    prediction = Prediction.query.get(prediction_id)
    if prediction and prediction.user_id == current_user.id:
        # Create the email content
        msg = Message('Your Car Price Prediction Result',
                      recipients=[current_user.email])
        msg.body = f"""
        Hello {current_user.username},

        Here is the prediction for your car:

        - Company: {prediction.company}
        - Model: {prediction.car_model}
        - Year: {prediction.year}
        - Fuel Type: {prediction.fuel_type}
        - Kilometers Driven: {prediction.kilometers_driven}
        - Predicted Price: ₹{prediction.predicted_price}

        Thank you for using our service!
        """
        
        # Send the email
        try:
            mail.send(msg)
            flash('Prediction details sent to your email!', 'success')
        except Exception as e:
            flash(f'Error sending email: {e}', 'danger')
    
    return redirect(url_for('profile'))

@app.route('/delete_prediction/<int:prediction_id>', methods=['POST'])
@login_required
def delete_prediction(prediction_id):
    prediction = Prediction.query.get(prediction_id)
    if prediction and prediction.user_id == current_user.id:
        db.session.delete(prediction)
        db.session.commit()
        flash('Prediction deleted successfully!', 'success')
    else:
        flash('Prediction not found or permission denied!', 'danger')
    
    return redirect(url_for('profile'))



@app.route('/update_profile', methods=['GET', 'POST'])
@login_required
def update_profile():
    # Your logic here   
    if request.method == 'POST':
        # Get updated data from the form
        username = request.form['username']
        email = request.form['email']
        
        # Update the current user data in the database
        current_user.username = username
        current_user.email = email

        try:
            db.session.commit()
            flash('Profile updated successfully', 'success')
            return redirect(url_for('profile'))
        except:
            flash('Error updating profile', 'danger')

    return render_template('update_profile.html', user_info={'username': current_user.username, 'email': current_user.email})

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('landingpage'))

@app.route('/')
@login_required
def dashboard():
    return render_template('index.html', name=current_user.username)

@app.route('/landing')
def landingpage():
    return render_template('landing_page.html')  # Render the landing page HTML file


@app.route('/predict', methods=['POST'])
@login_required
def predict():
    try:
        company = request.form.get('company')
        car_model = request.form.get('car_models')
        year = request.form.get('year')
        fuel_type = request.form.get('fuel_type')
        driven = request.form.get('kilo_driven')

        prediction = model.predict(pd.DataFrame(
            columns=['name', 'company', 'year', 'kms_driven', 'fuel_type'],
            data=np.array([car_model, company, year, driven, fuel_type]).reshape(1, 5)
        ))

        predicted_price = np.round(prediction[0], 2)

        # Save the prediction to the database
        new_prediction = Prediction(
            user_id=current_user.id,
            company=company,
            car_model=car_model,
            year=int(year),
            fuel_type=fuel_type,
            kilometers_driven=int(driven),
            predicted_price=predicted_price
        )
        db.session.add(new_prediction)
        db.session.commit()

        return f"The predicted price is ₹{predicted_price}"

    except Exception as e:
        print(f"Error during prediction: {e}")
        return "An error occurred while making the prediction."


@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/EMI')
def emi():
    return render_template('EMI.html')

if __name__ == '__main__':
    # Ensure the database is created before running the app
    if not os.path.exists('users.db'):
        with app.app_context():
            db.create_all()

    app.run(debug=True)

from flask import Flask, render_template, flash, request, redirect, url_for
from wtforms import Form, TextField, TextAreaField, validators, StringField, SubmitField
from flask import Flask 
from flask_sqlalchemy import SQLAlchemy 
from datetime import datetime
from password_encryption import encrypt_password, check_encrypted_password
from otp import generateOTP
import smtplib

app = Flask(__name__)
app.config.from_object(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
app.config['SECRET_KEY'] = '7d441f27d441f27567d441f2b6176a'
db = SQLAlchemy(app)
DEBUG = True

# Create database model for data storage
class User(db.Model):
    username = db.Column(db.String(50), nullable=False,)
    password = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), primary_key=True)
    number = db.Column(db.String(50), nullable=True)

# Inserting values into table
def insertUser(username, password, email, number= None):
    me = User(username=username, password=password, email=email, number= number)
    db.session.add(me)
    db.session.commit()

# URL for main page  
@app.route("/")
def user():
    return render_template('layout.html')

@app.route("/success/<email>/<otp>")
def success(email,otp):
    return f"<h1>{'Welcome! '+email+' successfully logged in'}</h1>"



@app.route("/validateotp/<email>/<genOtp>", methods=['GET', 'POST'])
def validateotp(email, genOtp):
    if request.method == 'POST':
        entered_otp= request.form['otpgenerator']
        otp_check= check_encrypted_password(entered_otp, genOtp)
        if otp_check:
            return redirect(url_for('success', email=email, otp=entered_otp))
        else:
            return f"<h1>{'Incorrect OTP'}</h1> <nav> <a href='/login'>Go back to login</a>"

    return render_template('otp.html')
    

# URL for first time registration users
@app.route("/register", methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name=request.form['username']
        password=request.form['password']
        email=request.form['email']
        number= request.form['number'] 

        # Verification of user in database
        user_check= User.query.filter_by(email=email).first()
        
        # If user is not present make registration
        if user_check is None:

            # Password encryption before passing data to database
            encrypt_pass= encrypt_password(password)
            insertUser(username= name, password=encrypt_pass, email=email, number=number)
            return f"<h1>{'Welcome! '+name+' with email '+email+' is successfully registered'}</h1>"
        else:
            # If user is present redirect to login page
            return f"<h1>{'User already exists'}</h1> <nav> <a href='/login'>Go back to login</a>"
 
    else:
        return render_template('register.html')


@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email=request.form['email']
        password=request.form['password']

        # Verification of user in database
        user_name = User.query.filter_by(email=email).first()
        
        # If user is not present 
        if user_name is None:
            return f"<h1>{'Invalid login credentials'}</h1> <nav> <a href='/login'>Go back to login</a>"
        if user_name is not None:
            # If user present then verify if password entered is correct
            encr_user_password= user_name.password
            validation= check_encrypted_password(password, encr_user_password)
            # If password verification is true 
            if validation:
                s = smtplib.SMTP('smtp.gmail.com', 587) 
                s.starttls() 
                s.login("prajwalgarla143@gmail.com", "Prajwal@143")
                gen_otp= generateOTP() 
                encrypt_otp= encrypt_password(gen_otp)
                message =  "The OPT is {} ".format(gen_otp)
                s.sendmail("prajwalgarla143@gmail.com", email, message) 
                s.quit()
                return redirect(url_for('validateotp', email=email, genOtp=encrypt_otp))
            else:
                return f"<h1>{'Invalid login credentials'}</h1> <nav> <a href='/login'>Go back to login</a>"
    else:
        return render_template('login.html')

if __name__ == "__main__":
    # Host address and port 
    app.run()
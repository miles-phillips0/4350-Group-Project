import os
from flask_login import(login_user, LoginManager,login_required, logout_user,current_user,) 
from flask import Flask, flash, redirect, render_template, url_for
from flask_sqlalchemy import SQLAlchemy
import flask
from dotenv import load_dotenv, find_dotenv

#Loading .env Postgres DB & Secret Keys
load_dotenv(find_dotenv())

app = flask.Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
if app.config['SQLALCHEMY_DATABASE_URI'].startswith("postgres://"):
    app.config['SQLALCHEMY_DATABASE_URI'] = app.config["SQLALCHEMY_DATABASE_URI"].replace("postgres://", "postgresql://")
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")



app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
#Created table for Users to be added to

class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    userName = db.Column(db.String(120), nullable=False)

db.create_all()

#Flask Login Manager 
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "signin"

@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))

#Register Method
@app.route('/', methods=["GET", "POST"])
@login_required
def index():
    if flask.request.method == "POST":
        data = flask.request.form
        newUser = Users(userName= data["r_username"] )

        # Flask form for Username 
        db.session.add(newUser)
        db.session.commit()
    return flask.render_template( "login.html")

#Signin Method
@app.route('/signin', methods = ["GET","POST"])
def signin():
    
    if flask.request.method == "POST":
        
        print(flask.request.form.get('username'))
        u_name= flask.request.form.get('username')
        if Users.query.filter_by(userName=u_name).first():
            flash("User Authenticated")
            print("User Found")
            return flask.render_template( "index.html")
            
        else:  
            flash("User Not Found")
            print("User Not found", u_name)
            return flask.render_template("login.html")


    return flask.render_template("login.html")



@app.route('/logout')
def logout():
    logout_user()
    flash('You were logged out.')
    return redirect(url_for('signin'))


app.run(
    host=os.getenv('IP', '0.0.0.0'),
    port=int(os.getenv('PORT', 8080)),
    debug=True
    
)

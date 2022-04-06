import os
from flask_login import(login_user, LoginManager,login_required, logout_user,current_user,) 
import requests
from flask import Flask, flash, redirect, render_template, url_for
from flask_sqlalchemy import SQLAlchemy
import flask


app = flask.Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
if app.config['SQLALCHEMY_DATABASE_URI'].startswith("postgres://"):
    app.config['SQLALCHEMY_DATABASE_URI'] = app.config["SQLALCHEMY_DATABASE_URI"].replace("postgres://", "postgresql://")
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")   



app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    userName = db.Column(db.String(120), nullable=False)

db.create_all()

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "signin"



import os
from flask_login import (
    login_user,
    LoginManager,
    login_required,
    logout_user,
    current_user,
)
from flask import Flask, flash, redirect, render_template, url_for
from flask_sqlalchemy import SQLAlchemy
import flask
from dotenv import load_dotenv, find_dotenv
import bcrypt
from sqlalchemy.dialects.postgresql import BYTEA

#Loading .env Postgres DB & Secret Keys
load_dotenv(find_dotenv())

app = flask.Flask(__name__)

app.config["SEND_FILE_MAX_AGE_DEFAULT"] = 0
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("HEROKU_POSTGRESQL_IVORY_URL")
if app.config["SQLALCHEMY_DATABASE_URI"].startswith("postgres://"):
    app.config["SQLALCHEMY_DATABASE_URI"] = app.config[
        "SQLALCHEMY_DATABASE_URI"
    ].replace("postgres://", "postgresql://")


app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")


app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)
#Created table for Users to be added to


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), nullable=False)
    hash = db.Column(BYTEA, nullable=False)


db.create_all()

#Flask Login Manager 
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "signin"


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route("/", methods=["GET", "POST"])
def index():
    if flask.request.method == "POST":
        data = flask.request.form
        email = data["r_email"]
        password = data["r_password"]
        if email == "":
            flash("Email Not Entered")
            return flask.render_template("login.html")
        if password == "":
            flash("Password Not Entered")
            return flask.render_template("login.html")

        if not User.query.filter_by(email=email).first():
            hashed = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
            newUser = User(email=email, hash=hashed)
            db.session.add(newUser)
            db.session.commit()
            return flask.render_template("login.html")
        flash(f"{email} is already registered")

    return flask.render_template("login.html")



@app.route("/signin", methods=["GET", "POST"])

def signin():

    if flask.request.method == "POST":

        data = flask.request.form
        email = data["email"]
        password = data["password"]
        if email == "":
            flash("Email Not Entered")
            return flask.render_template("login.html")
        if password == "":
            flash("Password Not Entered")
            return flask.render_template("login.html")
        user = User.query.filter_by(email=email).first()

        if user:
            if bcrypt.checkpw(password.encode("utf-8"), user.hash):
                return flask.render_template("index.html")

        else:
            flash("User not found")

    return flask.render_template("login.html")


@app.route("/logout")
def logout():
    logout_user()
    flash("You were logged out.")
    return redirect(url_for("signin"))


app.run(host=os.getenv("IP", "0.0.0.0"), port=int(os.getenv("PORT", 8080)), debug=True)

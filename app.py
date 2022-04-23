"""Python file to run to create the app"""
# pylint: disable=no-member, missing-function-docstring, assigning-non-slot
import os
import flask
from flask import flash, redirect, url_for
from flask_login import (
    LoginManager,
    UserMixin,
    login_user,
    login_required,
    logout_user,
    current_user,
)
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv, find_dotenv
import bcrypt
from sqlalchemy.dialects.postgresql import BYTEA
from NBA_API import (
    get_player_id,
    get_player_games_between_dates,
    get_advanced_player_info,
)

# Loading .env Postgres DB & Secret Keys
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
# Created table for Users to be added to


class Users(UserMixin, db.Model):
    """Creates the DB model for Users"""

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), nullable=False)
    hash = db.Column(BYTEA, nullable=False)
    roster = db.Column(db.String(120), default="")


# db.create_all()

# Flask Login Manager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "signup"


@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))


@app.route("/", methods=["GET", "POST"])
def index():
    return flask.render_template("entrance.html")


@app.route("/search", methods=["GET", "POST"])
def search():
    if flask.request.method == "POST":
        data = flask.request.form
        player_name = data["playerSearch"]
        player_id = get_player_id(player_name)
        player_game_log = get_player_games_between_dates(
            "12/25/2020", "12/25/2021", player_id
        )

        try:
            emptydf = player_game_log.empty

        except AttributeError:
            return flask.redirect("/search")

        if emptydf:
            return flask.redirect("/search")

        avg_points = round(player_game_log["PTS"].mean(), 2)
        avg_rebounds = round(player_game_log["REB"].mean(), 2)
        avg_assists = round(player_game_log["AST"].mean(), 2)
        return flask.render_template(
            "search.html",
            len_results=1,
            player_name=player_name,
            avg_assists=avg_assists,
            avg_points=avg_points,
            avg_rebounds=avg_rebounds,
            user=current_user,
            player_id=player_id,
        )

    return flask.render_template(
        "search.html",
        len_results=0,
        user=current_user,
    )


# Routing to homepage
@app.route("/main", methods=["GET", "POST"])
def main():
    return flask.redirect("/home")


# Trying to have an app bar routing Below is my attempt
# _----------------------------------------------------------
@app.route("/login", methods=["GET", "POST"])
def login():
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
        user = Users.query.filter_by(email=email).first()
        if user:
            if bcrypt.checkpw(password.encode("utf-8"), user.hash):
                login_user(user)
                return flask.redirect("/home")

            flash(f"Incorrect Password for {email}")
            return flask.render_template("login.html")

        flash("User not found")

    return flask.render_template("login.html")


@app.route("/signup", methods=["GET", "POST"])
def signup():
    if flask.request.method == "POST":
        data = flask.request.form
        email = data["r_email"]
        password = data["r_password"]
        if email == "":
            flash("Email Not Entered")
            return flask.render_template("signup.html")
        if password == "":
            flash("Password Not Entered")
            return flask.render_template("signup.html")

        if not Users.query.filter_by(email=email).first():
            hashed = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
            new_user = Users(email=email, hash=hashed, roster="")
            db.session.add(new_user)
            db.session.commit()
            flash("User Registered")

            return flask.render_template("login.html")
        flash(f"{email} is already registered")

    return flask.render_template("signup.html")


# -----------------------------------------------------------


@app.route("/logout")
def logout():
    logout_user()
    flash("You were logged out.")
    return redirect(url_for("login"))


@app.route("/home", methods=["GET", "POST"])
@login_required
def home():
    roster = current_user.roster.split(";")
    len_roster = len(roster)
    if len_roster == 1 and roster[0] == "":
        len_roster -= 1
    player_names = [""] * len_roster
    time_frame = [""] * len_roster
    pts = [0] * len_roster
    ast = [0] * len_roster
    reb = [0] * len_roster
    pie = [0] * len_roster
    height = [0] * len_roster
    weight = [0] * len_roster
    team = [0] * len_roster
    jersey = [0] * len_roster
    position = [0] * len_roster
    if len_roster > 0:
        for i in range(0, len_roster):
            (
                player_names[i],
                time_frame[i],
                pts[i],
                ast[i],
                reb[i],
                pie[i],
                height[i],
                weight[i],
                team[i],
                jersey[i],
                position[i],
            ) = get_advanced_player_info(roster[i])
    return flask.render_template(
        "index.html",
        user=current_user,
        len_roster=len_roster,
        player_names=player_names,
        time_frame=time_frame,
        pts=pts,
        ast=ast,
        reb=reb,
        pie=pie,
        height=height,
        weight=weight,
        team=team,
        jersey=jersey,
        position=position,
        roster=roster,
    )


@app.route("/delete", methods=["GET", "POST"])
@login_required
def delete_player():
    if flask.request.method == "POST":
        data = flask.request.form
        deleted_player = data["player"]
        roster = current_user.roster.split(";")
        if deleted_player in roster:
            roster.remove(deleted_player)
        new_roster = ""
        for player in roster:
            if len(new_roster) == 0:
                new_roster += player
            else:
                new_roster += f";{player}"
        current_user.roster = new_roster
        db.session.commit()

    return flask.redirect("/home")


#  Adding Players to Roster
@app.route("/add", methods=["GET", "POST"])
@login_required
def add_player():
    if flask.request.method == "POST":
        data = flask.request.form
        roster = current_user.roster.split(";")
        new_player_id = str(data["btn_id"])
        if len(current_user.roster) == 0:
            current_user.roster += new_player_id
        elif new_player_id not in roster:
            current_user.roster += f";{new_player_id}"
        else:
            return flask.redirect("/home")
        db.session.commit()

    return flask.redirect("/home")


app.run(
    host=os.getenv("IP", "0.0.0.0"), port=int(os.getenv("PORT", "8080")), debug=True
)

from flask import Flask, render_template, request, url_for, flash, redirect
from flask_pymongo import PyMongo
from dotenv import load_dotenv
import datetime
import os

load_dotenv()

app = Flask(__name__)

app.config["MONGO_URI"] = os.getenv("MONGO_URI")
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")

mongodb = PyMongo()
mongodb.init_app(app)
db = mongodb.db

@app.route("/")
def Home():
    all_notes = list(db.notes.find())[::-1]
    return render_template("home.html", notes=all_notes)

@app.route("/entry/", methods=["POST"])
def create_entry():
    if request.method == "POST":
        if request.form.get("note_content") != "" and request.form.get("note_title") != "":
            current_date = datetime.datetime.today().strftime("%Y-%m-%d")
            db.notes.insert_one({
                "title": request.form.get("note_title"),
                "content": request.form.get("note_content"),
                "date": current_date,
                "better_date": datetime.datetime.strptime(current_date, "%Y-%m-%d").strftime("%b %d")
            })
        else:
            flash("Note content and title cannot be empty.", "danger")

    return redirect(url_for("Home"))

app.run(debug=True)
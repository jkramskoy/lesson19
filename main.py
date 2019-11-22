# GET and a POST request handler

from flask import Flask, render_template, request, make_response,redirect,url_for
from models import User, db
import random

app = Flask(__name__)
db.create_all() # create (new) tables in the database

@ app.route("/")
def index():
    return render_template ("/index.html")


@ app.route("/populate", methods=["POST"])
def populate():
    name = request.form.get("user-name")
    email = request.form.get("user-email")
    secret_number = random.randint(1,30)

    user=User(name=name,email=email,secret_number=secret_number)

    db.add(user)
    db.commit()
    return render_template("index.html")



@app.route("/guess",methods=["POST"])
def guess():
    user_guess = int(request.form.get("guess"))
    email = request.form.get("user-email")

    user = db.query(User).filter_by(email=email).first()
    if user:
        guess = user.secret_number
        if guess == user_guess:
            return render_template("result.html", flag="your guess was correct")
        elif guess > user_guess:
            return render_template("result.html", flag="your guess too low")
        else:
            return render_template("result.html", flag="your guess too high")
    else:
        return render_template("result.html", flag="User was not found")



if __name__== "__main__":
    app.run(debug=True,port=5750)




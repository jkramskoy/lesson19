# GET and a POST request handler

from flask import Flask, render_template, request, make_response,redirect,url_for
from models import User, db
import random
import uuid
import hashlib

app = Flask(__name__)
db.create_all() # create (new) tables in the database

@ app.route ("/")
def index():
    session_token = request.cookies.get("session_token")

    if session_token:
        user = db.query(User).filter_by(session_token=session_token).first()
    else:
        user = None
    return render_template("index.html", user=user)


@app.route("/populate", methods=["POST"])
def populate():
    name = request.form.get("user-name")
    email = request.form.get("user-email")
    password = request.form.get("user-password")
    print(password)
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    secret_number = random.randint(1, 30)

    # check if user already exists
    user = db.query(User).filter_by(email=email).first()

    if not user:
        # create User object
        user = User(name=name, email=email, secret_number=secret_number, password=hashed_password)
        # add to db
        db.add(user)
        db.commit()

    if hashed_password != user.password:
        return "WRONG PASSWORD! Go back and try again."

    session_token = str(uuid.uuid4())
    user.session_token = session_token
    db.add(user)
    db.commit()

    response = make_response(redirect(url_for("index")))
    response.set_cookie("session_token", session_token, httponly=True, samesite='Strict')

    return response


@app.route("/guess", methods=["POST"])
def guess():
    user_guess = int(request.form.get("guess"))
    session_token = request.cookies.get("session_token")

    user = db.query(User).filter_by(session_token=session_token).first()
    if user:
        guess = user.secret_number
        if guess == user_guess:
            return render_template("result.html", flag="Your Guess was Correct")
        elif guess > user_guess:
            return render_template("result.html", flag="Your Guess was too low")
        else:
            return render_template("result.html", flag="Your Guess was too high")
    else:
        return render_template("result.html", flag="User was not found")


if __name__== "__main__":
    app.run(debug=True,port=5750)




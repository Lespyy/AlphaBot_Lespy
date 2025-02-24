from flask import Flask, render_template, request, redirect, url_for, make_response
import sqlite3
import hashlib
import jwt
import datetime
from alpha_bot import AlphaBot

#I create the app
app = Flask(__name__)
Secret_key = "Exploding_kittens"

#I add the alphaBot calling it Lespy and I stop him
Lespy = AlphaBot()
Lespy.stop()


"""When I am in INDEX, the main one"""
@app.route("/", methods=['GET', 'POST'])
def index():

    """I control the robot and every part of his moovements"""

    #I stop it just for be safe
    Lespy.stop()

    # I take the token from the cookie and I check it
    token = request.cookies.get("token")
    if not token:
        return redirect(url_for('login'))
    else:
        print(token)
    
    try:
        decoded_token = jwt.decode(token, Secret_key, algorithms=["HS256"])
        email = decoded_token["email"]  # Assicurati di usare "email" anche nel token
    except jwt.ExpiredSignatureError:
        return redirect(url_for("login"))
    except jwt.InvalidTokenError:
        return redirect(url_for("login"))

    # If I receive a POST request I check the command
    if request.method == 'POST':
        if request.form.get('action') == 'Logout':
            response = make_response(redirect(url_for('login')))
            response.delete_cookie("token")
            return response
        else:
            command_handler(request.form.get('action'))
            
    return render_template("index.html")


def command_handler(command):

    """Here I check the commands and do what they say"""

    if  command == 'W':
        print("W pressed")
        Lespy.forward()

    elif request.form.get('action') == 'A':
        print("A pressed")
        Lespy.left()

    elif request.form.get('action') == 'S':
        print("S pressed")
        Lespy.backward()

    elif request.form.get('action') == 'D':
        print("D pressed")
        Lespy.right()

    elif request.form.get('action') == 'O':
        Lespy.stop()
        print("Stop pressed")
        
    else:
        print("Unknown action")


"""Used in LOGIN page"""
@app.route('/login', methods=['GET', 'POST'])
def login():

    """Here I check and accept the credentials"""

    #If I receive a POST request I take the credentials and check'em
    if request.method == 'POST':
        email = request.form.get('e-mail')
        psw = request.form.get('password')
        return check(email, psw)
    Lespy.stop()
    return render_template('login.html')

def check(email, psw):

    """here I go inside the db and check if the credentials are valid
    
        !I don't insert the clear password but I put inside just the digest!
    """

    db_name = "database.db"
    with sqlite3.connect(db_name) as conn:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT email, password FROM Users WHERE email = ? AND password = ?",
            (email, hashlib.sha256(psw.encode()).hexdigest())
        )
        result = cursor.fetchone()
        if result is None:
            print("Access denied")
            return render_template("login.html", alert="Invalid credentials")
        else:
            #if the acces is allowed I create the tocken and with the cookie
            print("Access allowed")
            response = make_response(redirect(url_for('index')))
            expiration = datetime.datetime.utcnow() + datetime.timedelta(days=1)
            token = jwt.encode({"email": email, "exp": expiration}, Secret_key, algorithm="HS256")
            response.set_cookie("token", token, max_age=60*60*24)
            print(f"token1: {token}")
            return response

"""Used in CREATE ACCOUNT page"""
@app.route('/create_account', methods=['GET', 'POST'])
def create_account():

    db_name = "database.db"

    """Here I create the account ready to be used"""

    #if POST request take email and add in the db the credentials 
    if request.method == 'POST':
        email = request.form.get('e-mail')
        psw = request.form.get('password')
        
        with sqlite3.connect(db_name) as conn:
            cursor = conn.cursor()
            hashed_psw = hashlib.sha256(psw.encode()).hexdigest()
            cursor.execute("INSERT INTO Users (email, password) VALUES (?, ?)", (email, hashed_psw))
            conn.commit()
            print("Account successfully created")
        return redirect(url_for('login'))
    Lespy.stop()
    return render_template('create_account.html')

#I start the whole app
if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")


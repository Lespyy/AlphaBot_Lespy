from flask import Flask, render_template, request, redirect, url_for, make_response
import sqlite3
import hashlib
import jwt
import datetime

from alpha_bot import AlphaBot

app = Flask(__name__)
Secret_key = "fablab"


Lespy = AlphaBot()

current_left_speed = 0
current_right_speed = 0

@app.route("/", methods=['GET', 'POST'])
def index():
    global current_left_speed, current_right_speed

    # Recupera il token dal cookie
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

    # Gestione dei comandi del robot
    if request.method == 'POST':
        if request.form.get('action') == 'W':
            print("W pressed")
            current_left_speed -= 50
            current_right_speed += 50
            Lespy.setMotor(left = current_left_speed, right = current_right_speed)

        elif request.form.get('action') == 'A':
            print("A pressed")
            current_left_speed -= 25
            current_right_speed += 50
            Lespy.setMotor(left = current_left_speed, right = current_right_speed)

        elif request.form.get('action') == 'S':
            print("S pressed")
            current_left_speed += 50
            current_right_speed -= 50
            Lespy.setMotor(left = current_left_speed, right = current_right_speed)

        elif request.form.get('action') == 'D':
            print("D pressed")
            current_left_speed -= 50
            current_right_speed += 25
            Lespy.setMotor(left = current_left_speed, right = current_right_speed)

        elif request.form.get('action') == 'O':
            current_left_speed = 0
            current_right_speed = 0
            Lespy.setMotor(left = current_left_speed, right = current_right_speed)
            print("Stop pressed")

        elif request.form.get('action') == 'Logout':
            response = make_response(redirect(url_for('login')))
            response.delete_cookie("token")
            return response

        else:
            print("Unknown action")
            
    return render_template("index.html")

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('e-mail')
        psw = request.form.get('password')
        return check(email, psw)
    Lespy.stop()
    return render_template('login.html')

def check(email, psw):
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
            print("Access allowed")
            response = make_response(redirect(url_for('index')))
            expiration = datetime.datetime.utcnow() + datetime.timedelta(days=1)
            # Usa "email" in minuscolo per coerenza
            token = jwt.encode({"email": email, "exp": expiration}, Secret_key, algorithm="HS256")
            response.set_cookie("token", token, max_age=60*60*24)
            print(f"token1: {token}")
            return response

@app.route('/create_account', methods=['GET', 'POST'])
def create_account():
    if request.method == 'POST':
        email = request.form.get('e-mail')
        psw = request.form.get('password')
        db_name = "database.db"
        
        with sqlite3.connect(db_name) as conn:
            cursor = conn.cursor()
            hashed_psw = hashlib.sha256(psw.encode()).hexdigest()
            cursor.execute("INSERT INTO Users (email, password) VALUES (?, ?)", (email, hashed_psw))
            conn.commit()
            print("Account successfully created")
        return redirect(url_for('login'))
    Lespy.stop()
    return render_template('create_account.html')

if __name__ == '__main__':
    app.run(debug=True)


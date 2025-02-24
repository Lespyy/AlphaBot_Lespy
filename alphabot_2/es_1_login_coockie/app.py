from flask import Flask, render_template, request, redirect, url_for, make_response
import sqlite3
import hashlib


#from alpha_bot import AlphaBot


#creo il flask
app = Flask(__name__)
#Lespy = AlphaBot()

current_left_speed = 0
current_right_speed = 0

#Metodo index
@app.route("/", methods=['GET', 'POST'])
def index():
    global current_left_speed, current_right_speed
    
    """
    Carica l'index.html
    dove ritorno i comandi del robot
    """

    email = request.cookies.get("email")  # Recupera il cookie "username"
    if not email:
        return redirect(url_for('login'))


    if request.method == 'POST':
        # Controlla quale pulsante è stato premuto
        if request.form.get('action') == 'W':
            print("W pressed")
            current_left_speed -= 50
            current_right_speed += 50
            print(f"right: {current_right_speed}")
            print(f"left: {current_left_speed}")

            
        elif request.form.get('action') == 'A':
            print("A pressed")
            current_left_speed -= 25
            current_right_speed += 50
            #Lespy.setMotor(current_left_speed, current_right_speed)
            print(f"right: {current_right_speed}")
            print(f"left: {current_left_speed}")


        elif request.form.get('action') == 'S':
            print("S pressed")
            current_left_speed += 50
            current_right_speed -= 50
            #Lespy.setMotor(current_left_speed, current_right_speed)
            print(f"right: {current_right_speed}")
            print(f"left: {current_left_speed}")


        elif request.form.get('action') == 'D':
            print("D pressed")
            current_left_speed -= 50
            current_right_speed += 25
            #Lespy.setMotor(current_left_speed, current_right_speed)
            print(f"right: {current_right_speed}")
            print(f"left: {current_left_speed}")


        elif request.form.get('action') == 'O':
            current_left_speed = 0
            current_right_speed = 0
            print("stop pressed")
            #Lespy.setMotor(current_left_speed, current_right_speed)
            print(f"right: {current_right_speed}")
            print(f"left: {current_left_speed}")

        elif request.form.get('action') == 'Logout':
            response = make_response(redirect(url_for('login')))
            response.delete_cookie("email")  # Rimuove il cookie "username"
            return response

        else:
            print("Unknown action")
            
    return render_template("index.html")

#Metodo Login
@app.route('/login', methods=['GET', 'POST'])
def login():

    """
    Guarda le credenziali che gli mando via POST 
    controlla se sono all'interno del db
    e nel caso mi resetta la pagina login (Denied)
    oppure mi fa accedere a index.html
    """

    

    if request.method == 'POST':
        email = request.form.get('e-mail')
        psw = request.form.get('password')
        
        return check(email, psw)
        
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
                return render_template("login.html", alert = "Invalid credential")
            else:
                print("Access allowed")
                response = make_response(redirect(url_for('index')))
                response.set_cookie("email", email, max_age = 60*60*24)
            
                return response

#Metodo Create account
@app.route('/create_account', methods=['GET', 'POST'])
def create_account():
    """
        Controlla le credenziali che gli mando e le salva automaticamente nel db 

        !ATTENZIONE!
        Per un motivo di sicurezza io non salverò MAI la psw dell'utente 
        per evitare che possa essere compremessa negli altri siti 

        ma salverà il digest di essa così da renderla inutile solo per quel sito 
    """
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
    return render_template('create_account.html')

if __name__ == '__main__':
    app.run(debug=True)


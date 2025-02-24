from flask import Flask, render_template, request
app = Flask(__name__)

@app.route("/", methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Controlla quale pulsante è stato premuto
        if request.form.get('action') == 'W':
            print("W pressed")
            
        elif request.form.get('action') == 'A':
            print("A pressed")
            
        elif request.form.get('action') == 'S':
            print("S pressed")
            
        elif request.form.get('action') == 'D':
            print("D pressed")
            
        elif request.form.get('action') == 'O':
            print("stop pressed")
            
        else:
            print("Unknown action")
            
    return render_template("index.html")

if __name__ == '__main__':
    app.run(debug=True, host='localhost')

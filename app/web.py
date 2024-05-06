# file web.py

from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/", methods=['GET'])
def saluda():
    return render_template('index.html', msg="Hola Mundo!")

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080, debug=True)



from flask import Flask, render_template



app = Flask(__name__)

@app.route('/')
def index():
    titulo = 'IEVN'
    list = ['pedro', 'mario', 'giezy']
    return render_template('index.html',titulo = titulo, list = list)

@app.route('/hola')
def hola():
    return 'JELOUUUUU'

@app.route("/user/<string:user>")
def user(user):
    return 'HOLA USUARIO, COMO ESTAS: ' + user

@app.route("/numero/<int:n>")
def numero(n):
    return 'NUMERO: {}'.format(n)

@app.route("/user/<int:id>/<string:username>")
def username(id, username):
    return "ID: {} Nombre: {}".format(id,username)

@app.route("/suma/<float:n1>/<float:n2>")
def suma(n1, n2):
    return "LA SUMA ES: {}".format(n1 + n2)

@app.route("/default")
@app.route("/default/string:n")
def default(n = 'juan'):
    return "EL VALOR DE N ES :" + n



if __name__ == "__main__":
    app.run(debug=True)

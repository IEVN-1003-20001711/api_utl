from flask import Flask, jsonify
from flask_mysqldb import MySQL
from config import config

app = Flask(__name__)

con = MySQL(app)



#FORMA PARA HACER LA CONECCION EN UN SERVIDOR DE MYSQL
@app.route('/alumnos', methods = ['GET'])
def list_alumnos():
    try:
        cursor = con.connection.cursor()
        sql = 'select * from alumnos'
        cursor.execute(sql)
        datos = cursor.fetchall()
        listAlum = []
        for fila in datos:
            alum = {'matricula':fila[0],
                    'nombre':fila[1],
                    'apaterno':fila[2],
                    'amaterno':fila[3],
                    'correo':fila[4]}
            listAlum.append(alum)
        #print(listAlum)
        return jsonify({'Alumnos':listAlum,'mensaje':'Lista de Alumnos'})

    except Exception as ex:
        return jsonify({'mensaje': '{}'.format(ex)})




@app.route('/alumnos/<mat>', methods = ['GET'])
def leer_alumno(mat):
    try:
        cursor = con.connection.cursor()
        sql = "select * from alumnos where matricula {0}".format(mat)
        cursor.execute(sql)
        datos = cursor.fetchall()
        print(datos)
    except Exception as ex:
        return jsonify({'mensaje': '{}'.format(ex)})



def pagina_no_encontrada(error):
    return '<h1> PAGINA NO ENCONTRADA MASTER </h1>',404



if __name__ == "__main__":
    app.config.from_object(config['development'])
    app.register_error_handler(404, pagina_no_encontrada)
    app.run()
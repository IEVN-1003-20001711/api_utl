from flask import Flask, jsonify, request
from flask_mysqldb import MySQL
from config import config

app = Flask(__name__)

con = MySQL(app)


def leer_alumno_bd(math):
    try:
        cursor = con.connection.cursor()
        sql = "select * from alumnos where matricula = {0}".format(math)
        cursor.execute(sql)
        datos = cursor.fetchone()
        if datos != None:
            alumno = {'matricula':datos[0],
                    'nombre':datos[1],
                    'apaterno':datos[2],
                    'amaterno':datos[3],
                    'correo':datos[4]}
            return alumno
        else:
            return None

    except Exception as ex:
        raise ex



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




@app.route('/alumnos/<math>', methods = ['GET'])
def leer_alumno(math):
    try:
        alumno = leer_alumno_bd(math)
        if alumno != None:
            return jsonify({'Alumnos': alumno, 'mensaje': 'el alumno fue encontrado','exito':True})
        else:
            return jsonify({'Alumnos': alumno, 'mensaje': 'el alumno NO se encontró', 'exito':False})

    except Exception as ex:
        return jsonify({'mensaje': '{}'.format(ex), 'exito':False})



@app.route('/alumnos', methods = ['POST'])
def registrar_alumno():
    try:
        alumno = leer_alumno_bd(request.json['matricula'])

        if alumno != None:
            return jsonify({'mensaje':'El Alumno YA EXISTE','exito':False})
        else:
            cursor = con.connection.cursor()
            sql = """INSERT INTO Alumnos(matricula,nombre,apaterno,amaterno,correo)
            VALUES({0}, '{1}','{2}','{3}','{4}')""".format(request.json['matricula'],
            request.json['nombre'], request.json['apaterno'], request.json['amaterno'],
            request.json['correo'])
            cursor.execute(sql)
            con.connection.commit()
            return jsonify({'mensaje':'Alumno Registrado', 'exito':True})

    except Exception as ex:
        return jsonify({'mensaje': '{}'.format(ex)})
    

@app.route('/alumnos/<math>',methods=['PUT'])
def actualizar_alumno(math):
    try:
        alumno = leer_alumno_bd(math)

        if alumno != None:
            cursor = con.connection.cursor()
            sql = """UPDATE alumnos SET nombre = '{0}',apaterno='{1}',
            amaterno='{2}', correo='{3}' where matricula='{4}'""".format(request.json['nombre'],
                                                                          request.json['apaterno'],
                                                                          request.json['amaterno'],
                                                                          request.json['correo'],
                                                                          math)
            cursor.execute(sql)
            con.connection.commit()
            return jsonify({'mensaje':'Alumno ACTUALIZADO', 'exito':True})

    except Exception as ex:
        return jsonify({'mensaje': '{}'.format(ex)})
    



@app.route('/alumnos/<math>', methods = ['DELETE'])
def eliminar_alumno(math):
    try:
        alumno = leer_alumno_bd(math)
        if alumno != None:
            cursor = con.connection.cursor()
            sql = 'DELETE FROM alumnos WHERE matricula = {0}'.format(math)
            cursor.execute(sql)
            con.connection.commit()
            return jsonify({'Alumnos': alumno, 'mensaje': 'El alumno ha sido eliminado','exito':True})
        else:
            return jsonify({'Alumnos': alumno, 'mensaje': 'el alumno NO se encontró', 'exito':False})

    except Exception as ex:
        return jsonify({'mensaje': '{}'.format(ex), 'exito':False})




def pagina_no_encontrada(error):
    return '<h1> PAGINA NO ENCONTRADA MASTER </h1>',404


if __name__ == "__main__":
    app.config.from_object(config['development'])
    app.register_error_handler(404, pagina_no_encontrada)
    app.run()
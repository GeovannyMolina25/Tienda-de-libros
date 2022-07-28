
from fileinput import filename
import os
from flask import Flask
from flask import render_template, request,redirect
from flaskext.mysql import MySQL
from datetime import datetime
from flask import send_from_directory

app=Flask(__name__)

mysql=MySQL()

app.config['MYSQL_DATABASE_HOST']='localhost'
app.config['MYSQL_DATABASE_USER']='root'
app.config['MYSQL_DATABASE_PASSWORD']=''
app.config['MYSQL_DATABASE_DB']='sitio'
mysql.init_app(app)



@app.route('/')
def inicio():
    return render_template('sitio/index.html')

@app.route('/img/<imagen>')
def imagenes(imagen):
    print(imagen)
    return send_from_directory(os.path.join('templates/sitio/img'),imagen)




@app.route('/libros')
def libros():
    return render_template('sitio/libros.html')

@app.route('/nosotros')
def cabecera():
    return render_template('sitio/nosotros.html')

@app.route('/admin/')
def admin_index():
    return render_template('admin/index.html')

@app.route('/admin/login')
def admin_login():
    return render_template('admin/login.html')

@app.route('/admin/libros')
def admin_libros():
    conexion=mysql.connect()
    cursor=conexion.cursor()
    cursor.execute("SELECT * FROM `libro`" )
    libros=cursor.fetchall()
    conexion.commit()
    print(libros)
    return render_template('admin/libros.html',libros=libros)

@app.route('/admin/libros/guardar', methods=['POST'])
def admin_libros_guardar():
    _nombre=request.form['txtNombre']
    _url=request.form['txtURL']
    _archivo=request.files['txtImagen']
    
    tiempo = datetime.now()
    horaActual=tiempo.strftime('%Y%H%M%S')

    if _archivo.filename!="":
        nuevoNombre=horaActual+"_"+_archivo.filename
        _archivo.save("templates/sitio/img/"+nuevoNombre)


    sql="INSERT INTO `libro` (`id`, `nombre`, `imagen`, `url`) VALUES (NULL, %s,%s,%s);"
    datos=(_nombre,nuevoNombre,_url)
    conexion=mysql.connect()
    cursor=conexion.cursor()
    cursor.execute(sql,datos)
    conexion.commit()
    
    print(_nombre)
    print(_url)
    print(_archivo)
    return redirect('/admin/libros')

@app.route('/admin/libros/borrar', methods=['POST'])
def admin_libros_borrar():
    _id=request.form['txtID']
    print(_id)
    conexion=mysql.connect()
    cursor=conexion.cursor()
    cursor.execute("SELECT * FROM `libro` WHERE id=%s",(_id) )
    libro=cursor.fetchall()
    conexion.commit()
    print(libro)

    conexion=mysql.connect()
    cursor=conexion.cursor()
    cursor.execute("DELETE FROM libro WHERE id=%s",(_id) )
    conexion.commit()
    return redirect('/admin/libros')
    

if __name__ =='__main__':
    app.run(debug=True)

from flask import Flask, render_template,request,redirect,url_for,flash
from flask_mysqldb import MySQL
from flask import send_from_directory
from datetime import datetime
import os 


app = Flask(__name__)

# Configuración de la base de datos
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '123456789'
app.config['MYSQL_DB'] = 'vicman_bikes'
mysql = MySQL(app)

# BACKEND USER

@app.route('/user/index')
def index_user():
    # Conexión y ejecución del SQL
    conn = mysql.connection
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM vehiculo WHERE idCategoria=1")
    vehiculos0 = cursor.fetchall()
    # Conexión y ejecución del SQL para obtener las vehiculos por categoria
    cursor.execute("SELECT * FROM vehiculo WHERE idCategoria=2")
    vehiculos1 = cursor.fetchall()
    cursor.execute("SELECT * FROM vehiculo WHERE idCategoria=3")
    vehiculos2 = cursor.fetchall()
    conn.commit()
    # Retorna html con datos
    return render_template('user/index.html',vehiculos0=vehiculos0, vehiculos1=vehiculos1, vehiculos2=vehiculos2)

@app.route('/user/vehiculo/<int:id>')
def mostrar_vehiculo(id):
    # Conexión y ejecución del SQL
    conn = mysql.connection
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM vehiculo WHERE idVehiculo=%s", (id,))
    vehiculos = cursor.fetchall()
    conn.commit()
    return render_template('user/producto.html', vehiculos=vehiculos) 


# BACKEND ADMIN


#Permitir entrar a la carpeta imagen, y guardar la ruta de la carpeta
CARPETA=os.path.join('uploads')
app.config['CARPETA']=CARPETA
#Permite traer y mostrar la foto de la carpeta uploads
@app.route('/uploads/<nombreFoto>')
def uploads(nombreFoto):
    return send_from_directory(app.config['CARPETA'],nombreFoto)

#Admin Cliente

@app.route('/admin/clientes')
def index_clientes():
    #Connexion y ejecucion del SQL
    sql = "SELECT * FROM cliente;"
    conn = mysql.connection
    cursor = conn.cursor()
    cursor.execute(sql)
    clientes = cursor.fetchall()
    conn.commit()
    #retorna html con datos
    return render_template('admin/clientes/index.html', clientes=clientes)


@app.route('/admin/destroy_cliente/<identificacion>')
def destroy_cliente(identificacion):
    conn = mysql.connection
    cursor = conn.cursor()
    cursor.execute("DELETE FROM cliente WHERE identificacion=%s", (identificacion,))
    conn.commit()
    return redirect('/admin/clientes')

@app.route('/admin/edit_cliente/<identificacion>')
def edit_cliente(identificacion):
    conn = mysql.connection
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM cliente WHERE identificacion=%s", (identificacion,))
    clientes = cursor.fetchall()
    conn.commit()
    return render_template('admin/clientes/edit.html', clientes=clientes)

@app.route('/admin/update_cliente', methods=['POST'])
def update_cliente():
    _identificacion = request.form['txtIdentificacion']
    _nombre = request.form['txtNombre']
    _apellido = request.form['txtApellido']
    _telefono = request.form['txtTelefono']
    _correo = request.form['txtCorreo']
    _contraseña = request.form['txtContraseña']
    
    sql = "UPDATE cliente SET nombre=%s, apellido=%s, telefono=%s, correo=%s, contraseña=%s WHERE identificacion=%s;"
    datos = (_nombre, _apellido, _telefono, _correo, _contraseña, _identificacion)
    
    conn = mysql.connection
    cursor = conn.cursor()
    cursor.execute(sql, datos)
    conn.commit()
    
    return redirect('/admin/clientes')

@app.route('/admin/create_cliente')
def create_cliente():
    return render_template('admin/clientes/create.html')

@app.route('/admin/store_cliente', methods=['POST'])
def store_cliente():
    _identificacion = request.form['txtIdentificacion']
    _nombre = request.form['txtNombre']
    _apellido = request.form['txtApellido']
    _telefono = request.form['txtTelefono']
    _correo = request.form['txtCorreo']
    _contraseña = request.form['txtContraseña']
    
    sql = "INSERT INTO cliente (identificacion, nombre, apellido, telefono, correo, contraseña) VALUES (%s, %s, %s, %s, %s, %s);"
    datos = (_identificacion, _nombre, _apellido, _telefono, _correo, _contraseña)
    
    conn = mysql.connection
    cursor = conn.cursor()
    cursor.execute(sql, datos)
    conn.commit()
    
    return redirect('/admin/clientes')

@app.route('/admin/show_cliente/<string:identificacion>')
def show_cliente(identificacion):
    # Conexión y ejecución del SQL
    conn = mysql.connection
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM cliente WHERE identificacion=%s", (identificacion,))
    clientes = cursor.fetchall()
    conn.commit()
    # Retorna HTML con datos
    return render_template('admin/clientes/read.html', clientes=clientes)

#Admin Categoria

@app.route('/admin/categoria')
def index_categoria():
    # Conexión y ejecución del SQL
    sql = "SELECT * FROM categoria;"
    conn = mysql.connection
    cursor = conn.cursor()
    cursor.execute(sql)
    categorias = cursor.fetchall()
    conn.commit()
    # Retorna HTML con datos
    return render_template('admin/categoria/index.html', categorias=categorias)

@app.route('/admin/destroy_categoria/<int:id>')
def destroy_categoria(id):
    # Conexión y ejecución del SQL
    conn = mysql.connection
    cursor = conn.cursor()
    cursor.execute("DELETE FROM categoria WHERE idCategoria=%s", (id,))
    conn.commit()
    # Redirecciona
    return redirect('/admin/categoria')

@app.route('/admin/edit_categoria/<int:id>')
def edit_categoria(id):
    # Conexión y ejecución del SQL
    conn = mysql.connection
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM categoria WHERE idCategoria=%s", (id,))
    categorias = cursor.fetchall()
    conn.commit()
    # Retorna HTML con datos
    return render_template('admin/categoria/edit.html', categorias=categorias)

@app.route('/admin/show_categoria/<int:id>')
def show_categoria(id):
    # Conexión y ejecución del SQL
    conn = mysql.connection
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM categoria WHERE idCategoria=%s", (id,))
    categorias = cursor.fetchall()
    conn.commit()
    # Retorna HTML con datos
    return render_template('admin/categoria/read.html', categorias=categorias)

@app.route('/admin/update_categoria', methods=['POST'])
def update_categoria():
    # Recibir datos del usuario
    _categoria = request.form['txtCategoria']
    id = request.form['txtId']
    # Consulta SQL
    sql = "UPDATE categoria SET categoria=%s WHERE idCategoria=%s;"
    datos = (_categoria, id)
    # Conexión y ejecución del SQL
    conn = mysql.connection
    cursor = conn.cursor()
    cursor.execute(sql, datos)
    conn.commit()
    # Redirige
    return redirect('/admin/categoria')

@app.route('/admin/create_categoria')
def create_categoria():
    # Retornar HTML
    return render_template('admin/categoria/create.html')

@app.route('/admin/store_categoria', methods=['POST'])
def storage_categoria():
    # Recibir datos del usuario
    _categoria = request.form['txtCategoria']
    # Consulta SQL
    sql = "INSERT INTO categoria (categoria) VALUES (%s);"
    datos = (_categoria,)
    # Conexión y ejecución del SQL
    conn = mysql.connection
    cursor = conn.cursor()
    cursor.execute(sql, datos)
    conn.commit()
    # Retorno HTML
    return redirect('/admin/categoria')
    
#Backend Vehiculo

@app.route('/admin/vehiculo')
def index_vehiculo():
    # Conexión y ejecución del SQL
    sql = "SELECT * FROM vehiculo;"
    conn = mysql.connection
    cursor = conn.cursor()
    cursor.execute(sql)
    vehiculos = cursor.fetchall()
    conn.commit()
    # Retorna html con datos
    return render_template('admin/vehiculos/index.html', vehiculos=vehiculos)

@app.route('/admin/destroy_vehiculo/<int:id>')
def destroy_vehiculo(id):
    # Conexión 
    conn = mysql.connection
    cursor = conn.cursor()
    # Busco la foto del objeto y lo elimino de la carpeta uploads
    cursor.execute("SELECT foto FROM vehiculo WHERE idVehiculo=%s", (id,))
    fila = cursor.fetchall()
    os.remove(os.path.join(app.config['CARPETA'], fila[0][0]))
    # Ejecución del SQL
    cursor.execute("DELETE FROM vehiculo WHERE idVehiculo=%s", (id,))
    conn.commit()
    # Redirecciona
    return redirect('/admin/vehiculo')

@app.route('/admin/edit_vehiculo/<int:id>')
def edit_vehiculo(id):
    # Conexión y ejecución del SQL
    conn = mysql.connection
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM vehiculo WHERE idVehiculo=%s", (id,))
    vehiculos = cursor.fetchall()
    # Conexión y ejecución del SQL para obtener las categorías
    cursor.execute("SELECT * FROM categoria;")
    categorias = cursor.fetchall()
    conn.commit()
    # Retorna html con datos
    return render_template('admin/vehiculos/edit.html', vehiculos=vehiculos, categorias=categorias)

@app.route('/admin/show_vehiculo/<int:id>')
def show_vehiculo(id):
    # Conexión y ejecución del SQL
    conn = mysql.connection
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM vehiculo WHERE idVehiculo=%s", (id,))
    vehiculos = cursor.fetchall()
    cursor.execute("""
        SELECT categoria.*
        FROM categoria
        JOIN vehiculo ON categoria.idCategoria = vehiculo.idCategoria
        WHERE vehiculo.idVehiculo=%s
    """, (id,))
    categoria = cursor.fetchone()  # Obtener solo un registro
    conn.commit()
    # Retorna html con datos
    return render_template('admin/vehiculos/read.html', vehiculos=vehiculos, categoria=categoria)

@app.route('/admin/update_vehiculo', methods=['POST'])
def update_vehiculo():
    # Recibir datos del usuario
    _nombre = request.form['txtNombre']
    _precio = request.form['txtPrecio']
    _stock = request.form['txtStock']
    _detalles = request.form['txtDetalles']
    _foto = request.files['txtFoto']
    _idCategoria = request.form['txtIdCategoria']
    id = request.form['txtIdvehiculo']
    # Consulta SQL
    sql = "UPDATE vehiculo SET nombre=%s, precio=%s, stock=%s, detalles=%s, idCategoria=%s WHERE idVehiculo=%s;"
    datos = (_nombre, _precio, _stock, _detalles,_idCategoria, id)
    # Conexión 
    conn = mysql.connection
    cursor = conn.cursor()
    # Obtener el tiempo de subida del archivo
    now = datetime.now()
    tiempo = now.strftime("%Y%H%M%S")
    # Verificar que hay una imagen
    if _foto.filename != '':
        # Guardo la nueva imagen en uploads
        nuevoNombreFoto = tiempo + _foto.filename
        _foto.save("uploads/" + nuevoNombreFoto)
        # Busco la foto anterior y la elimino de la carpeta uploads
        cursor.execute("SELECT foto FROM vehiculo WHERE idVehiculo=%s", id)
        fila = cursor.fetchall()
        os.remove(os.path.join(app.config['CARPETA'], fila[0][0]))
        # Actualizo el nuevo nombre de la foto en la base de datos
        cursor.execute("UPDATE vehiculo SET foto=%s WHERE idVehiculo=%s", (nuevoNombreFoto, id))
        conn.commit()
    # Ejecución del SQL (actualizo el resto del objeto)
    cursor.execute(sql, datos)
    conn.commit()
    
    # Redirigir
    return redirect('/admin/vehiculo')

@app.route('/admin/create_vehiculo')
def create_vehiculo():
    sql = "SELECT * FROM categoria;"
    conn = mysql.connection
    cursor = conn.cursor()
    cursor.execute(sql)
    categorias = cursor.fetchall()
    conn.commit()
    # Retornar HTML
    return render_template('admin/vehiculos/create.html',categorias=categorias)

@app.route('/admin/store_vehiculo', methods=['POST'])
def storage_vehiculo():
    # Recibir datos del usuario
    _nombre = request.form['txtNombre']
    _precio = request.form['txtPrecio']
    _stock = request.form['txtStock']
    _detalles = request.form['txtDetalles']
    _foto = request.files['txtFoto']
    _idCategoria=request.form['txtIdCategoria']
    # Obtener el tiempo de subida del archivo
    now = datetime.now()
    tiempo = now.strftime("%Y%H%M%S")
    # Cambiar nombre del archivo y guardarlo en la aplicación
    if _foto.filename != '':
        nuevoNombreFoto = tiempo + _foto.filename
        _foto.save("uploads/" + nuevoNombreFoto)
    # Consulta SQL
    sql = "INSERT INTO vehiculo (nombre, precio, stock, detalles, foto, idCategoria) VALUES (%s, %s, %s, %s, %s, %s);"
    datos = (_nombre, _precio, _stock, _detalles, nuevoNombreFoto, _idCategoria)
    # Conexión y ejecución del SQL
    conn = mysql.connection
    cursor = conn.cursor()
    cursor.execute(sql, datos)
    conn.commit()
    # Retorno html
    return redirect('/admin/vehiculo')

#Backend Factura

@app.route('/admin/factura')
def index_factura():
    # Conexión y ejecución del SQL
    sql = "SELECT * FROM factura;"
    conn = mysql.connection
    cursor = conn.cursor()
    cursor.execute(sql)
    facturas = cursor.fetchall()
    conn.commit()
    # Retorna html con datos
    return render_template('admin/factura/index.html', facturas=facturas)

@app.route('/admin/destroy_factura/<int:id>')
def destroy_factura(id):
    # Conexión y ejecución del SQL
    conn = mysql.connection
    cursor = conn.cursor()
    cursor.execute("DELETE FROM factura WHERE idFactura=%s", (id,))
    conn.commit()
    # Redirecciona
    return redirect('/admin/factura')

@app.route('/admin/edit_factura/<int:id>')
def edit_factura(id):
    # Conexión y ejecución del SQL
    conn = mysql.connection
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM factura WHERE idFactura=%s", (id,))
    facturas = cursor.fetchall()
    conn.commit()
    # Retorna html con datos
    return render_template('admin/factura/edit.html', facturas=facturas)

@app.route('/admin/show_factura/<int:id>')
def show_factura(id):
    # Conexión y ejecución del SQL
    conn = mysql.connection
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM factura WHERE idFactura=%s", (id,))
    facturas = cursor.fetchall()
    conn.commit()
    # Retorna html con datos
    return render_template('admin/factura/read.html', facturas=facturas)

@app.route('/admin/update_factura', methods=['POST'])
def update_factura():
    # Recibir datos del usuario
    _fecha = request.form['txtFecha']
    _identificacion = request.form['txtIdentificacion']
    _idVehiculo = request.form['txtIdvehiculo']
    id = request.form['txtIdfactura']

    # Consulta SQL
    sql = "UPDATE factura SET fecha=%s, identificacion=%s, idVehiculo=%s WHERE idFactura=%s;"
    datos = (_fecha, _identificacion, _idVehiculo, id)

    # Conexión y ejecución del SQL
    conn = mysql.connection
    cursor = conn.cursor()
    cursor.execute(sql, datos)
    conn.commit()

    # Redirigir
    return redirect('/admin/factura')

@app.route('/admin/create_factura')
def create_factura():
    # Retornar HTML
    return render_template('admin/factura/create.html')

@app.route('/admin/store_factura', methods=['POST'])
def storage_factura():
    _fecha = datetime.now().strftime('%Y-%m-%d')
    _identificacion = request.form['txtIdentificacion']
    _idVehiculo = request.form['txtIdvehiculo']

    # Consulta para verificar el stock del vehículo
    sql_check_stock = "SELECT stock FROM vehiculo WHERE idVehiculo = %s;"
    
    # Consulta SQL para insertar la factura
    sql_factura = "INSERT INTO factura (fecha, identificacion, idVehiculo) VALUES (%s, %s, %s);"
    
    # Consulta SQL para actualizar el stock del vehículo
    sql_update_stock = "UPDATE vehiculo SET stock = stock - 1 WHERE idVehiculo = %s;"

    conn = mysql.connection
    cursor = conn.cursor()

    try:
        # Verificar el stock del vehículo
        cursor.execute(sql_check_stock, (_idVehiculo,))
        stock_result = cursor.fetchone()
        
        if stock_result and stock_result[0] > 0:
            # Si el stock es mayor que 0, crear la factura y actualizar el stock
            cursor.execute(sql_factura, (_fecha, _identificacion, _idVehiculo))
            cursor.execute(sql_update_stock, (_idVehiculo,))
            conn.commit()  # Confirmar la transacción
        else:
            # Si el stock es 0 o menor, evitar crear la factura
            conn.rollback()  # Revertir cualquier cambio
            
            return redirect('/admin/factura')

    except Exception as e:
        conn.rollback()  # Deshacer la transacción en caso de error
        
        return redirect('/admin/factura')
    finally:
        cursor.close()

    # Retornar a la página principal
    return redirect('/admin/factura') 
    


#Main
if __name__ == '__main__':
    app.run(debug=True)

from flask import Flask, render_template, request, jsonify
from database import Database
from datetime import datetime


app = Flask(__name__)


# Instancia global de la base de datos
db = Database()


# Conectar al iniciar la aplicación
if db.conectar():
    print("[OK] Base de datos conectada al iniciar la app")
else:
    print("[ERROR] Error al conectar la base de datos")


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/api/registrar', methods=['POST'])
def registrar():
    """Registrar un nuevo equipo EN LA BASE DE DATOS MYSQL"""
    try:
        # Intentar obtener datos como JSON primero, luego como form-data
        if request.is_json:
            datos = request.get_json()
            print("[DEBUG] Datos recibidos como JSON")
        else:
            datos = request.form.to_dict()
            print("[DEBUG] Datos recibidos como FORM")
       
        print(f"[DEBUG] Datos completos: {datos}")
        print(f"\n[+] Registrando: {datos.get('codigo')}")
       
        # Validar que se recibieron datos
        if not datos or not datos.get('codigo'):
            print("[ERROR] No se recibieron datos o falta el código")
            return jsonify({
                'success': False,
                'error': 'No se recibieron datos del formulario o falta el código'
            }), 400
       
        # Guardar DIRECTAMENTE en MySQL
        if db.guardar_registro(datos):
            print(f"[OK] Registro guardado en MySQL")
            return jsonify({
                'success': True,
                'message': 'Registro guardado exitosamente en la base de datos'
            }), 201
        else:
            print(f"[ERROR] Error al guardar en MySQL")
            return jsonify({
                'success': False,
                'error': 'Error al guardar en la base de datos'
            }), 500
           
    except Exception as e:
        print(f"[ERROR] en /api/registrar: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400


@app.route('/api/registros', methods=['GET'])
def obtener_registros():
    """Obtener TODOS los registros de MySQL"""
    try:
        registros = db.obtener_todos_registros()
       
        # Convertir datetime a strings para JSON
        for reg in registros:
            if 'fecha_creacion' in reg and reg['fecha_creacion']:
                reg['fecha_creacion'] = reg['fecha_creacion'].isoformat()
            if 'fecha_mantenimiento' in reg and reg['fecha_mantenimiento']:
                reg['fecha_mantenimiento'] = reg['fecha_mantenimiento'].isoformat()
            if 'fecha_registro' in reg and reg['fecha_registro']:
                reg['fecha_registro'] = reg['fecha_registro'].isoformat()
       
        print(f"[OK] Se obtuvieron {len(registros)} registros de MySQL")
       
        return jsonify({
            'success': True,
            'data': registros,
            'total': len(registros)
        }), 200
       
    except Exception as e:
        print(f"[ERROR] en /api/registros: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/registros/<codigo>', methods=['GET'])
def obtener_registro(codigo):
    """Obtener UN registro específico por código"""
    try:
        registro = db.obtener_registro_por_codigo(codigo)
       
        if registro:
            if 'fecha_creacion' in registro and registro['fecha_creacion']:
                registro['fecha_creacion'] = registro['fecha_creacion'].isoformat()
            if 'fecha_mantenimiento' in registro and registro['fecha_mantenimiento']:
                registro['fecha_mantenimiento'] = registro['fecha_mantenimiento'].isoformat()
            if 'fecha_registro' in registro and registro['fecha_registro']:
                registro['fecha_registro'] = registro['fecha_registro'].isoformat()
           
            return jsonify({
                'success': True,
                'data': registro
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'Registro no encontrado'
            }), 404
           
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/registros/<codigo>', methods=['PUT'])
def actualizar_registro(codigo):
    """Actualizar un registro en MySQL"""
    try:
        if request.is_json:
            datos = request.get_json()
        else:
            datos = request.form.to_dict()
       
        if db.actualizar_registro(codigo, datos):
            return jsonify({
                'success': True,
                'message': 'Registro actualizado exitosamente'
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'Error al actualizar el registro'
            }), 500
           
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400


@app.route('/api/registros/<codigo>', methods=['DELETE'])
def eliminar_registro(codigo):
    """Eliminar un registro de MySQL"""
    try:
        if db.eliminar_registro(codigo):
            return jsonify({
                'success': True,
                'message': 'Registro eliminado exitosamente'
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'Error al eliminar el registro'
            }), 500
           
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400


@app.route('/api/registros/estado/<estado>', methods=['GET'])
def obtener_por_estado(estado):
    """Obtener registros filtrados por ESTADO"""
    try:
        registros = db.obtener_registros_por_estado(estado)
       
        for reg in registros:
            if 'fecha_creacion' in reg and reg['fecha_creacion']:
                reg['fecha_creacion'] = reg['fecha_creacion'].isoformat()
       
        return jsonify({
            'success': True,
            'data': registros,
            'total': len(registros)
        }), 200
       
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/registros/marca/<marca>', methods=['GET'])
def obtener_por_marca(marca):
    """Obtener registros filtrados por MARCA"""
    try:
        registros = db.obtener_registros_por_marca(marca)
       
        for reg in registros:
            if 'fecha_creacion' in reg and reg['fecha_creacion']:
                reg['fecha_creacion'] = reg['fecha_creacion'].isoformat()
       
        return jsonify({
            'success': True,
            'data': registros,
            'total': len(registros)
        }), 200
       
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/registros/tipo/<tipo_equipo>', methods=['GET'])
def obtener_por_tipo(tipo_equipo):
    """Obtener registros filtrados por TIPO DE EQUIPO"""
    try:
        registros = db.obtener_registros_por_tipo(tipo_equipo)
       
        for reg in registros:
            if 'fecha_creacion' in reg and reg['fecha_creacion']:
                reg['fecha_creacion'] = reg['fecha_creacion'].isoformat()
       
        return jsonify({
            'success': True,
            'data': registros,
            'total': len(registros)
        }), 200
       
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/buscar', methods=['POST'])
def buscar_registros():
    """Buscar registros por TÉRMINO (código, marca, modelo)"""
    try:
        if request.is_json:
            datos = request.get_json()
        else:
            datos = request.form.to_dict()
           
        termino = datos.get('termino', '')
       
        if not termino:
            return jsonify({
                'success': False,
                'error': 'Debe proporcionar un término de búsqueda'
            }), 400
       
        registros = db.buscar_registros(termino)
       
        for reg in registros:
            if 'fecha_creacion' in reg and reg['fecha_creacion']:
                reg['fecha_creacion'] = reg['fecha_creacion'].isoformat()
       
        return jsonify({
            'success': True,
            'data': registros,
            'total': len(registros)
        }), 200
       
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/estadisticas', methods=['GET'])
def obtener_estadisticas():
    """Obtener ESTADÍSTICAS de los registros"""
    try:
        stats = db.obtener_estadisticas()
       
        print(f"\n[OK] Estadisticas obtenidas:")
        print(f"   Total: {stats.get('total_equipos')}")
        print(f"   Activos: {stats.get('equipos_activos')}")
        print(f"   Inactivos: {stats.get('equipos_inactivos')}")
       
        return jsonify({
            'success': True,
            'data': stats
        }), 200
       
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.errorhandler(404)
def not_found(error):
    return jsonify({
        'success': False,
        'error': 'Ruta no encontrada'
    }), 404


@app.errorhandler(500)
def server_error(error):
    return jsonify({
        'success': False,
        'error': 'Error del servidor'
    }), 500


@app.teardown_appcontext
def cerrar_bd(error):
    """Cerrar conexión al terminar"""
    db.cerrar()


if __name__ == '__main__':
    print("\n" + "="*60)
    print("[APP] VALLEGRANDE - Sistema de Registro de Equipos")
    print("="*60)
    print("[URL] http://localhost:5000")
    print("[BD] Base de datos: Registro")
    print("[TABLE] Tabla: registros_productos")
    print("="*60 + "\n")
   
    app.run(host="0.0.0.0", port=5000, debug=True)


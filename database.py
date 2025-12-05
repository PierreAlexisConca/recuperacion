import mysql.connector
from mysql.connector import Error
from typing import List, Dict, Optional
from datetime import datetime




class Database:
    """Clase para manejar la tabla registros_productos con reconexión automática"""
   
    def __init__(self):
        self.host = "database-2.chrtzh6gakul.us-east-1.rds.amazonaws.com"
        self.user = "admin"
        self.password = "ConcaFlores312007"
        self.database = "Registro"
        self.port = 3306
        self.connection = None
        self.cursor = None


    def conectar(self) -> bool:
        """Conectar a la base de datos MySQL"""
        try:
            # Cerrar conexión anterior si existe
            if self.connection and self.connection.is_connected():
                self.connection.close()
           
            # Nueva conexión
            self.connection = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database,
                port=self.port,
                autocommit=False
            )
           
            self.cursor = self.connection.cursor()
            print(f"✓ Conectado a {self.database}")
            return True
           
        except Error as e:
            print(f"ERROR de conexion: {e}")
            self.connection = None
            self.cursor = None
            return False


    def verificar_conexion(self) -> bool:
        """Verificar si la conexión está activa, si no, reconectar"""
        try:
            if not self.connection or not self.connection.is_connected():
                print("[!] Reconectando a la base de datos...")
                return self.conectar()
            return True
        except:
            return self.conectar()


    def guardar_registro(self, datos: Dict) -> bool:
        """Guardar un nuevo registro"""
        if not self.verificar_conexion():
            return False


        try:
            query = """
            INSERT INTO registros_productos
            (codigo, marca, modelo, sistema_operativo, ram, almacenamiento,
             tipo_equipo, estado, fecha_mantenimiento, fecha_registro)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """


            # Manejo de fechas
            fecha_mantenimiento = datos.get('fecha_mantenimiento')
            if not fecha_mantenimiento or fecha_mantenimiento == '':
                fecha_mantenimiento = None  # Ahora la BD permite NULL
           
            fecha_registro = datos.get('fecha_registro')
            if not fecha_registro or fecha_registro == '':
                fecha_registro = datetime.now().strftime('%Y-%m-%d')


            valores = (
                datos.get('codigo'),
                datos.get('marca'),
                datos.get('modelo'),
                datos.get('sistema_operativo'),
                int(datos.get('ram', 0)),
                int(datos.get('almacenamiento', 0)),
                datos.get('tipo_equipo'),
                datos.get('estado'),
                fecha_mantenimiento,
                fecha_registro
            )


            print(f"[+] Insertando: {datos.get('codigo')}")
            print(f"[DEBUG] Valores: {valores}")
           
            self.cursor.execute(query, valores)
            self.connection.commit()
            print(f"[OK] {datos.get('codigo')} guardado")
            return True


        except Error as e:
            print(f"[ERROR] INSERT: {e}")
            print(f"[DEBUG] Datos recibidos: {datos}")
            if self.connection:
                self.connection.rollback()
            return False


    def obtener_todos_registros(self) -> List[Dict]:
        """Obtener todos los registros"""
        if not self.verificar_conexion():
            return []


        try:
            query = "SELECT * FROM registros_productos ORDER BY fecha_registro DESC"
            self.cursor.execute(query)
            resultados = self.cursor.fetchall()
           
            registros = []
            columnas = [desc[0] for desc in self.cursor.description]
           
            for fila in resultados:
                registro = dict(zip(columnas, fila))
                registros.append(registro)
           
            return registros


        except Error as e:
            print(f"[ERROR] SELECT: {e}")
            return []


    def obtener_registro_por_codigo(self, codigo: str) -> Optional[Dict]:
        """Obtener un registro por código"""
        if not self.verificar_conexion():
            return None


        try:
            query = "SELECT * FROM registros_productos WHERE codigo = %s"
            self.cursor.execute(query, (codigo,))
            resultado = self.cursor.fetchone()
           
            if resultado:
                columnas = [desc[0] for desc in self.cursor.description]
                return dict(zip(columnas, resultado))
           
            return None


        except Error as e:
            print(f"[ERROR] Busqueda por codigo: {e}")
            return None


    def obtener_registros_por_estado(self, estado: str) -> List[Dict]:
        """Obtener registros por estado"""
        if not self.verificar_conexion():
            return []


        try:
            query = "SELECT * FROM registros_productos WHERE estado = %s ORDER BY fecha_registro DESC"
            self.cursor.execute(query, (estado,))
            resultados = self.cursor.fetchall()
           
            registros = []
            columnas = [desc[0] for desc in self.cursor.description]
           
            for fila in resultados:
                registro = dict(zip(columnas, fila))
                registros.append(registro)
           
            return registros


        except Error as e:
            print(f"[ERROR] Busqueda por estado: {e}")
            return []


    def obtener_registros_por_marca(self, marca: str) -> List[Dict]:
        """Obtener registros por marca"""
        if not self.verificar_conexion():
            return []


        try:
            query = "SELECT * FROM registros_productos WHERE marca = %s ORDER BY fecha_registro DESC"
            self.cursor.execute(query, (marca,))
            resultados = self.cursor.fetchall()
           
            registros = []
            columnas = [desc[0] for desc in self.cursor.description]
           
            for fila in resultados:
                registro = dict(zip(columnas, fila))
                registros.append(registro)
           
            return registros


        except Error as e:
            print(f"[ERROR] Busqueda por marca: {e}")
            return []


    def obtener_registros_por_tipo(self, tipo_equipo: str) -> List[Dict]:
        """Obtener registros por tipo"""
        if not self.verificar_conexion():
            return []


        try:
            query = "SELECT * FROM registros_productos WHERE tipo_equipo = %s ORDER BY fecha_registro DESC"
            self.cursor.execute(query, (tipo_equipo,))
            resultados = self.cursor.fetchall()
           
            registros = []
            columnas = [desc[0] for desc in self.cursor.description]
           
            for fila in resultados:
                registro = dict(zip(columnas, fila))
                registros.append(registro)
           
            return registros


        except Error as e:
            print(f"[ERROR] Busqueda por tipo: {e}")
            return []


    def actualizar_registro(self, codigo: str, datos: Dict) -> bool:
        """Actualizar un registro"""
        if not self.verificar_conexion():
            return False


        try:
            query = """
            UPDATE registros_productos SET
            marca = %s, modelo = %s, sistema_operativo = %s,
            ram = %s, almacenamiento = %s, tipo_equipo = %s,
            estado = %s, fecha_mantenimiento = %s
            WHERE codigo = %s
            """


            # fecha_mantenimiento es NOT NULL en la BD
            fecha_mantenimiento = datos.get('fecha_mantenimiento')
            if not fecha_mantenimiento or fecha_mantenimiento == '':
                fecha_mantenimiento = datetime.now().strftime('%Y-%m-%d')


            valores = (
                datos.get('marca'),
                datos.get('modelo'),
                datos.get('sistema_operativo'),
                int(datos.get('ram', 0)),
                int(datos.get('almacenamiento', 0)),
                datos.get('tipo_equipo'),
                datos.get('estado'),
                fecha_mantenimiento,
                codigo
            )


            self.cursor.execute(query, valores)
            self.connection.commit()
            print(f"✓ {codigo} actualizado")
            return True


        except Error as e:
            print(f"[ERROR] UPDATE: {e}")
            if self.connection:
                self.connection.rollback()
            return False


    def eliminar_registro(self, codigo: str) -> bool:
        """Eliminar un registro"""
        if not self.verificar_conexion():
            return False


        try:
            query = "DELETE FROM registros_productos WHERE codigo = %s"
            self.cursor.execute(query, (codigo,))
            self.connection.commit()
            print(f"[OK] {codigo} eliminado")
            return True


        except Error as e:
            print(f"[ERROR] DELETE: {e}")
            if self.connection:
                self.connection.rollback()
            return False


    def obtener_estadisticas(self) -> Dict:
        """Obtener estadísticas"""
        if not self.verificar_conexion():
            return {}


        try:
            stats = {}


            self.cursor.execute("SELECT COUNT(*) FROM registros_productos")
            stats['total_equipos'] = self.cursor.fetchone()[0]


            self.cursor.execute("SELECT COUNT(*) FROM registros_productos WHERE estado = 'Activo'")
            stats['equipos_activos'] = self.cursor.fetchone()[0]


            self.cursor.execute("SELECT COUNT(*) FROM registros_productos WHERE estado = 'Inactivo'")
            stats['equipos_inactivos'] = self.cursor.fetchone()[0]


            self.cursor.execute("SELECT marca, COUNT(*) as cantidad FROM registros_productos GROUP BY marca")
            stats['equipos_por_marca'] = [
                {'marca': row[0], 'cantidad': row[1]}
                for row in self.cursor.fetchall()
            ]


            self.cursor.execute("SELECT tipo_equipo, COUNT(*) as cantidad FROM registros_productos GROUP BY tipo_equipo")
            stats['equipos_por_tipo'] = [
                {'tipo': row[0], 'cantidad': row[1]}
                for row in self.cursor.fetchall()
            ]


            return stats


        except Error as e:
            print(f"[ERROR] Estadisticas: {e}")
            return {}


    def buscar_registros(self, termino: str) -> List[Dict]:
        """Buscar registros"""
        if not self.verificar_conexion():
            return []


        try:
            termino_busqueda = f"%{termino}%"
            query = """
            SELECT * FROM registros_productos
            WHERE codigo LIKE %s
               OR marca LIKE %s
               OR modelo LIKE %s
            ORDER BY fecha_registro DESC
            """


            self.cursor.execute(query, (termino_busqueda, termino_busqueda, termino_busqueda))
            resultados = self.cursor.fetchall()
           
            registros = []
            columnas = [desc[0] for desc in self.cursor.description]
           
            for fila in resultados:
                registro = dict(zip(columnas, fila))
                registros.append(registro)
           
            return registros


        except Error as e:
            print(f"[ERROR] Busqueda: {e}")
            return []


    def cerrar(self):
        """Cerrar la conexion"""
        try:
            if self.cursor:
                self.cursor.close()
            if self.connection and self.connection.is_connected():
                self.connection.close()
                print("[OK] Conexion cerrada")
        except Exception as e:
            print(f"[ERROR] al cerrar conexion: {e}")




# Para pruebas
if __name__ == "__main__":
    db = Database()
   
    if db.conectar():
        print("\n=== PRUEBA DE CONEXIÓN ===")
        registros = db.obtener_todos_registros()
        print(f"Total de registros: {len(registros)}")
       
        if registros:
            print("\nPrimer registro:")
            print(registros[0])
       
        db.cerrar()
    else:
        print("[ERROR] No se pudo conectar")


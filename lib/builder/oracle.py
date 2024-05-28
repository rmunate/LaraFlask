import cx_Oracle
from typing import Dict
from lib.environment.config import Config
from lib.builder.collections import Collection
from lib.builder.fetch import Fetch

class Oracle:
    """
        Clase para interactuar con una base de datos Oracle.

        Permite realizar diversas operaciones como conectar, ejecutar consultas y procedimientos,
        así como insertar, actualizar y eliminar datos de la base de datos.

        Esta clase encapsula funcionalidades específicas de Oracle, proporcionando métodos simples
        y coherentes para interactuar con la base de datos.

        Se utiliza para abstraer la complejidad de la interacción directa con la base de datos,
        facilitando el desarrollo y mantenimiento de aplicaciones que utilizan Oracle como backend.
    """
    # Types
    STRING = cx_Oracle.STRING
    CLOB = cx_Oracle.CLOB

    # Diccionario para almacenar las instancias de conexiones Oracle.
    _instances: Dict[str, 'Oracle'] = {}
    connection = None

    def __new__(cls, connection='default'):
        """
            Método especial utilizado para crear nuevas instancias de la clase Oracle.
            Verifica si ya existe una instancia para la conexión especificada.
            Si no existe, crea una nueva instancia y la almacena en el diccionario de instancias.

            Args:
                connection (str): Nombre de la conexión. Por defecto, 'default'.
            Returns:
                Oracle: Instancia de la conexión Oracle.
        """
        if connection not in cls._instances:
            cls._instances[connection] = super().__new__(cls)
        return cls._instances[connection]

    def __init__(self, connection='default'):
        """
            Método de inicialización de la clase Oracle.

            Args:
                connection (str): El nombre de la conexión a utilizar. Por defecto, es 'default'.

            Raises:
                RuntimeError: Si no se encuentra una configuración de base de datos Oracle con el nombre proporcionado.
        """
        # Guardar el nombre de la conexion
        self.name_conecction = connection

        # Determinar el camino de conexion.
        dataConnection = Config.database(f"oracle.{connection}")

        # Garantizar que no se encuentre vacia
        if dataConnection is None:
            raise RuntimeError(f"[DB Oracle]: No se encontró una configuración de base de datos Oracle con el nombre: {connection}")

        # Definir las variables de conexion
        username = dataConnection["username"]
        password = dataConnection["password"]
        host = dataConnection["host"]
        service = dataConnection["service"]

        # Carga de valores de conexión.
        self.username = username
        self.password = password
        self.tns = f"(DESCRIPTION=(ADDRESS_LIST=(ADDRESS=(PROTOCOL=TCP)(HOST={host})(PORT=1521)))(CONNECT_DATA=(SERVICE_NAME={service})))"
        self.encoding = "UTF-8"
        self.nencoding = "UTF-8"


    def connect(self):
        """
            Método para establecer la conexión a la base de datos Oracle.

            Returns:
                cx_Oracle.Connection: La conexión establecida con la base de datos.

            Raises:
                RuntimeError: Si la conexión a la base de datos falla.
        """
        if not self.connection or self.connection is None:

            try:

                # Crea la conexion a la base de datos Oracle.
                self.connection = cx_Oracle.connect(
                    user=self.username,
                    password=self.password,
                    dsn=self.tns,
                    encoding=self.encoding,
                    nencoding=self.nencoding
                )

            except Exception as e:

                # Detiene la Ejecucion por Excepción
                raise RuntimeError(f"[DB Oracle]: Conexión Fallida, {e}")

        return self.connection

    def close(self):
        """
            Método para cerrar la conexión a la base de datos Oracle.

            Returns:
                None
        """

        if self.connection:

            # Cierra la conexion.
            self.connection.close()

            # Vaciar Valor de la conexion
            self.connection = None
            self._instances[self.name_conecction] = None

    def query(self, statement, params=None):
        """
            Método para ejecutar una consulta genérica en la base de datos Oracle.

            Args:
                statement (str): La consulta SQL a ejecutar.
                params (tuple, optional): Parámetros para la consulta SQL (si es necesario). Por defecto, es None.

            Returns:
                dict: Un diccionario con los encabezados y las filas de la respuesta de la base de datos.

            Raises:
                ValueError: Si la consulta SQL falla.
        """
        try:
            # Ejecucion de Query
            connection = self.connect()
            cursor = connection.cursor()
            if params:
                cursor.execute(statement, params)
            else:
                cursor.execute(statement)

            # Retorna una instancia de la clase Fetch
            return Fetch(cursor=cursor)

        except Exception as e:

            # Lanzar excepcion
            raise ValueError(f"[DB Oracle]: Query Fallido, {e}")

    def execute(self, statement, params=None):
        """
            Método para ejecutar una sentencia en la base de datos Oracle.

            Args:
                statement (str): La sentencia SQL a ejecutar.
                params (tuple, optional): Parámetros para la sentencia SQL (si es necesario). Por defecto, es None.

            Returns:
                bool: True si la ejecución fue exitosa.

            Raises:
                ValueError: Si la sentencia SQL falla.
        """
        try:
            # Ejecucion de la sentencia.
            connection = self.connect()
            cursor = connection.cursor()
            if params:
                cursor.execute(statement, params)
            else:
                cursor.execute(statement)
            connection.commit()

            # Retorna true como bandera de exito.
            return True

        except Exception as e:

            # Lanzar excepcion
            raise ValueError(f"[DB Oracle]: Sentencia Fallida, {e}")

    def executemany(self, statement, params):
        """
            Método para ejecutar una sentencia en la base de datos Oracle.
            Ejecucion masiva.

            Args:
                statement (str): La sentencia SQL a ejecutar.
                params (tuple): Parámetros para la sentencia SQL (si es necesario). Por defecto, es None.

            Returns:
                bool: True si la ejecución fue exitosa.

            Raises:
                ValueError: Si la sentencia SQL falla.
        """
        try:
            # Ejecucion de la sentencia.
            connection = self.connect()
            cursor = connection.cursor()
            cursor.executemany(statement, params)
            connection.commit()

            # Retorna true como bandera de exito.
            return True

        except Exception as e:

            # Lanzar excepcion
            raise ValueError(f"[DB Oracle]: Sentencia Fallida, {e}")

    def select(self, statement, params=None):
        """
            Método para ejecutar una consulta SELECT con retorno de datos indexados en la base de datos Oracle.

            Args:
                statement (str): La consulta SELECT a ejecutar.
                params (tuple, optional): Parámetros para la consulta SELECT (si es necesario). Por defecto, es None.

            Returns:
                list: Una lista de diccionarios representando las filas de la respuesta de la base de datos, con columnas indexadas por nombre.

            Raises:
                ValueError: Si la consulta SELECT falla.
        """
        try:
            # Ejecucion Select.
            connection = self.connect()
            cursor = connection.cursor()
            if params:
                cursor.execute(statement, params)
            else:
                cursor.execute(statement)

            # Convertir a diccionarios
            headers = [desc[0] for desc in cursor.description]
            rows = [dict(zip(headers, row)) for row in cursor.fetchall()]

            # Retorno de valores asociados.
            return Collection(data=rows)

        except Exception as e:

            # Lanzar excepcion
            raise ValueError(f"[DB Oracle]: Select Fallido, {e}")

    def insert(self, statement, params=None):
        """
            Método para insertar datos en la base de datos Oracle.

            Args:
                statement (str): La sentencia de inserción SQL a ejecutar.
                params (tuple, optional): Parámetros para la sentencia de inserción SQL (si es necesario). Por defecto, es None.

            Returns:
                int or bool: El último ID insertado si es aplicable, o True si la inserción no generó un ID.

            Raises:
                ValueError: Si la inserción de datos falla.
        """
        try:
            # Ejecucion inserción.
            connection = self.connect()
            cursor = connection.cursor()
            if params:
                cursor.execute(statement, params)
            else:
                cursor.execute(statement)
            connection.commit()

            # Retorna el ultimo ID insertado si es aplicable
            if cursor.lastrowid is not None:
                return cursor.lastrowid
            else:
                # Si la inserción no generó un ID, devuelve un valor indicativo, como True
                return True

        except Exception as e:

            # Lanzar excepcion
            raise ValueError(f"[DB Oracle]: Insert Fallido, {e}")

    def update(self, statement, params=None):
        """
            Método para actualizar registros en la base de datos Oracle.

            Args:
                statement (str): La sentencia de actualización SQL a ejecutar.
                params (tuple, optional): Parámetros para la sentencia de actualización SQL (si es necesario). Por defecto, es None.

            Returns:
                bool: True si la actualización fue exitosa.

            Raises:
                ValueError: Si la actualización de registros falla.
        """
        try:
            # Ejecucion de la actualizacion.
            connection = self.connect()
            cursor = connection.cursor()
            if params:
                cursor.execute(statement, params)
            else:
                cursor.execute(statement)
            connection.commit()

            # Retorna true como bandera de exito.
            return True

        except Exception as e:

            # Lanzar excepcion
            raise ValueError(f"[DB Oracle]: Update Fallido, {e}")

    def delete(self, statement, params=None):
        """
            Método para eliminar un registro de la base de datos Oracle.

            Args:
                statement (str): La sentencia de eliminación SQL a ejecutar.
                params (tuple, optional): Parámetros para la sentencia de eliminación SQL (si es necesario). Por defecto, es None.

            Returns:
                bool: True si la eliminación fue exitosa.

            Raises:
                ValueError: Si la eliminación de registros falla.
        """
        try:
            # Ejecuta la eliminación.
            connection = self.connect()
            cursor = connection.cursor()
            if params:
                cursor.execute(statement, params)
            else:
                cursor.execute(statement)
            connection.commit()

            # Bandera de proceso Exitoso
            return True

        except Exception as e:

            # Lanzar excepcion
            raise ValueError(f"[DB Oracle]: Delete Fallido, {e}")

    def packageProcess(self, spname, paramsIn=[], paramsOut=[]):
        """
            Método para ejecutar procedimientos en paquetes de la base de datos Oracle.

            Args:
                spname (str): El nombre del procedimiento almacenado en el paquete.
                paramsIn (list, optional): Lista de parámetros de entrada para el procedimiento. Por defecto, es una lista vacía.
                paramsOut (list, optional): Lista de parámetros de salida para el procedimiento. Por defecto, es una lista vacía.

            Returns:
                list: Una lista de valores correspondientes a los parámetros de salida del procedimiento.

            Raises:
                ValueError: Si la ejecución del procedimiento falla.
        """
        try:
            # Ejecuta la eliminación.
            connection = self.connect()
            cursor = connection.cursor()

            # Define las variables de enlace para los parámetros de salida
            bind_vars = [cursor.var(t) for t in paramsOut]

            # Ejecuta el procedimiento almacenado con los parámetros de entrada y salida
            cursor.callproc(str(spname).lower(), paramsIn + bind_vars)

            # Recupera los valores de los parámetros de salida
            output_values = [var.getvalue() for var in bind_vars]

            # Retorna los valores de los parámetros de salida
            return output_values

        except Exception as e:

            # Lanzar excepcion
            raise ValueError(f"[DB Oracle]: Delete Fallido, {e}")
import pyodbc
from typing import Dict
from lib.environment.config import Config
from lib.builder.collections import Collection
from lib.builder.fetch import Fetch

class SQLServer:
    """
    Clase para la conexión a la base de datos SQL Server.
    """

    # Diccionario para almacenar las instancias de conexiones SQL Server.
    _instances: Dict[str, 'SQLServer'] = {}
    connection = None

    def __new__(cls, connection='default'):
        """
        Método especial utilizado para crear nuevas instancias de la clase SQLServer.

        Este método verifica si ya existe una instancia para la conexión especificada.
        Si no existe, crea una nueva instancia y la almacena en el diccionario de instancias.

        Args:
            connection (str): El nombre de la conexión a la base de datos. Por defecto, es 'default'.

        Returns:
            SQLServer: La instancia existente o una nueva instancia de la clase SQLServer.

        """
        if connection not in cls._instances:
            cls._instances[connection] = super().__new__(cls)
        return cls._instances[connection]

    def __init__(self, connection='default'):
        """
        Método de inicialización de la clase SQLServer.

        Este método inicializa una instancia de la clase SQLServer para establecer una conexión
        con la base de datos SQL Server utilizando los parámetros de conexión especificados.

        Args:
            connection (str): El nombre de la conexión a la base de datos. Por defecto, es 'default'.

        Raises:
            RuntimeError: Si no se encuentra una configuración de base de datos SQL Server con el nombre proporcionado.
        """

        # Determinar el camino de conexion.
        dataConnection = Config.database(f"sqlserver.{connection}")

        # Garantizar que no se encuentre vacia
        if dataConnection is None:
            raise RuntimeError(f"[DB SQL Server]: No se encontró una configuración de base de datos SQLServer con el nombre: {connection}")

        # Carga de valores de conexión.
        self.username = dataConnection["username"]
        self.password = dataConnection["password"]
        self.host = dataConnection["host"]
        self.database = dataConnection["database"]
        self.port = dataConnection["port"]

        # Cadena de conexión.
        self.conn_str = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={self.host},{self.port};DATABASE={self.database};UID={self.username};PWD={self.password};Charset=UTF-8'

    def connect(self):
        """
        Método para establecer la conexión a la base de datos SQL Server.

        Este método intenta crear una conexión a la base de datos SQL Server utilizando la cadena de conexión
        configurada en la instancia de la clase. Si la conexión no ha sido establecida previamente, se crea
        una nueva conexión utilizando la cadena de conexión y se devuelve.

        Returns:
            pyodbc.Connection: La conexión establecida a la base de datos SQL Server.

        Raises:
            ValueError: Si la conexión a la base de datos SQL Server falla.
        """
        if not self.connection or self.connection is None:
            try:

                # Crea la conexión a la base de datos SQL Server.
                self.connection = pyodbc.connect(self.conn_str)

            except Exception as e:

                # Lanzar Excepcion
                raise ValueError(f"[DB SQL Server]: Conexión fallida, {e}")

        return self.connection

    def close(self):
        """
        Método para cerrar la conexión a la base de datos SQL Server.

        Este método verifica si hay una conexión abierta y, si es así, la cierra. Luego, establece la
        variable de conexión a None para indicar que no hay una conexión activa.

        Returns:
            None
        """
        if self.connection:

            # Cierra la conexión.
            self.connection.close()

            # Valicar la conexion.
            self.connection = None

    def query(self, statement, params=None):
        """
        Método para ejecutar una consulta SQL genérica en la base de datos SQL Server.

        Este método ejecuta una consulta SQL proporcionada como argumento y devuelve los resultados,
        incluyendo los encabezados y las filas de la respuesta de la base de datos.

        Args:
            statement (str): La consulta SQL a ejecutar.
            params (tuple, optional): Parámetros para la consulta SQL (si es necesario). Por defecto, es None.

        Returns:
            dict: Un diccionario con los encabezados y las filas de la respuesta de la base de datos.

        Raises:
            ValueError: Si la ejecución de la consulta SQL falla.
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
            raise ValueError(f"[SQLServer]: Query Fallido, {e}")

    def execute(self, statement, params=None):
        """
        Método para ejecutar una sentencia SQL que no devuelve datos en la base de datos SQL Server.

        Este método ejecuta una sentencia SQL proporcionada como argumento y no espera resultados de la base de datos.
        Es útil para ejecutar operaciones de inserción, actualización o eliminación de datos.

        Args:
            statement (str): La sentencia SQL a ejecutar.
            params (tuple, optional): Parámetros para la sentencia SQL (si es necesario). Por defecto, es None.

        Returns:
            bool: True si la ejecución de la sentencia SQL fue exitosa.

        Raises:
            ValueError: Si la ejecución de la sentencia SQL falla.
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
            raise ValueError(f"[SQLServer]: Sentencia Fallida, {e}")

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
            raise ValueError(f"[SQLServer]: Sentencia Fallida, {e}")

    def select(self, statement, params=None):
        """
        Método para ejecutar una consulta SELECT en la base de datos SQL Server y devolver los resultados como una lista de diccionarios.

        Este método ejecuta una consulta SELECT proporcionada como argumento y devuelve los resultados como una lista de diccionarios,
        donde cada diccionario representa una fila de la respuesta de la base de datos y los nombres de las columnas son las claves.

        Args:
            statement (str): La consulta SELECT a ejecutar.
            params (tuple, optional): Parámetros para la consulta SELECT (si es necesario). Por defecto, es None.

        Returns:
            list: Una lista de diccionarios representando los resultados de la consulta SELECT.

        Raises:
            ValueError: Si la ejecución de la consulta SELECT falla.
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
            raise ValueError(f"[DB SQL Server]: Select Fallido, {e}")

    def insert(self, statement, params=None):
        """
        Método para realizar una inserción de datos en la base de datos SQL Server.

        Este método ejecuta una sentencia SQL de inserción proporcionada como argumento y, si es exitosa,
        devuelve el ID del último registro insertado. Si la inserción no generó un ID, se devuelve True
        como indicador de éxito.

        Args:
            statement (str): La sentencia SQL de inserción a ejecutar.
            params (tuple, optional): Parámetros para la sentencia SQL de inserción (si es necesario). Por defecto, es None.

        Returns:
            int or bool: El ID del último registro insertado si es aplicable, o True si la inserción fue exitosa.

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
            raise ValueError(f"[DB SQL Server]: Insert Fallido, {e}")

    def update(self, statement, params=None):
        """
        Método para actualizar registros en la base de datos SQL Server.

        Este método ejecuta una sentencia SQL de actualización proporcionada como argumento
        y actualiza los registros en la base de datos. Si la actualización es exitosa, devuelve True.

        Args:
            statement (str): La sentencia SQL de actualización a ejecutar.
            params (tuple, optional): Parámetros para la sentencia SQL de actualización (si es necesario). Por defecto, es None.

        Returns:
            bool: True si la actualización de los registros fue exitosa.

        Raises:
            ValueError: Si la actualización de los registros falla.
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
            raise ValueError(f"[DB SQL Server]: Update Fallido, {e}")

    def delete(self, statement, params=None):
        """
        Método para eliminar un registro de la base de datos SQL Server.

        Este método ejecuta una sentencia SQL de eliminación proporcionada como argumento
        y elimina el registro de la base de datos. Si la eliminación es exitosa, devuelve True.

        Args:
            statement (str): La sentencia SQL de eliminación a ejecutar.
            params (tuple, optional): Parámetros para la sentencia SQL de eliminación (si es necesario). Por defecto, es None.

        Returns:
            bool: True si la eliminación del registro fue exitosa.

        Raises:
            ValueError: Si la eliminación del registro falla.
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
            raise ValueError(f"[DB SQL Server]: Delete Fallido, {e}")
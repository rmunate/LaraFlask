from lib.builder.oracle import Oracle
from flask import jsonify

class DataTable:

    """
    Esta clase permite retornar valores para DataTables en la vista.
    Permite consultar los datos a nivel de vista (RECOMENDADO) o también con queries directos.
    """

    _db = None
    _connection = None
    _db_availables = ['oracle']
    _draw = None
    _serverside = True
    _table = None
    _query = None
    _columns = []
    _columns_string = None
    _start = 0
    _end = 10
    _limit = 10
    _search = None
    _conditionals = None
    _order_column = 1
    _order_direction = 'ASC'
    _statement = None
    _response = None

    def __init__(self, driver: str, connection='default', serverside=True, request=None):
        """
        Inicializa una instancia de DataTable.
        Actualmente solo pemite hacer consultas a Vistas. (Proximas Versiones Se Podra Hacer Query Directo)

        Args:
            driver (str): Tipo de base de datos a utilizar (ej. 'oracle', 'sqlsrv').
            connection (str, optional): Nombre de la conexión. Defaults to 'default'.
            serverside (bool, optional): Indica si se utiliza el procesamiento en el servidor. Defaults to True.
            request (dict, optional): Diccionario con los parámetros de la solicitud.
        """
        if not driver:
            raise ValueError("Se requiere definir una base de datos para la consulta.")
        elif driver not in self._db_availables:
            raise ValueError(f"La base de datos proporcionada no está soportada: {driver}")

        self._db = driver
        self._connection = connection
        self._serverside = serverside

        # Llama a métodos internos con valores del request
        if self._serverside:
            self.draw(request["draw"])
            self.start(request["start"])
            self.limit(request["length"])
            self.search(request["search"])
            self.order(
                column=int(request["order_column"]) + 1,
                orientation=request["order_dir"]
            )

    def draw(self, draw):
        """
        Establece el identificador único de la solicitud al backend.

        Args:
            draw: Identificador único de la solicitud.
        """
        self._draw = draw
        return self

    def _extract_name_columns(self):

        """
        Este metodo extrae las columnas de la consulta, aprovechandose de ejecutar una consulta
        con una sola linea de retorno.
        """

        statement = f"SELECT * FROM ({self._query}) SUBQUERY FETCH FIRST 1 ROW ONLY"
        if self._db == 'oracle':
            column_names = Oracle().query(statement).headers()
            self.columns(*column_names)

    def query(self, statement):

        """
        Estblece un query string sobre el cual se aplicará todo el proceso de consulta y tratamiento
        de datos segun se defina el comportamiento.
        """
        self._query = statement

        """Extraer Columnas"""
        self._extract_name_columns()

        return self

    def view(self, view: str):
        """
        Establece la vista de la base de datos a consultar.

        Args:
            view (str): Nombre de la vista.
        """
        self._table = str(view).strip().lower()
        return self

    def table(self, table: str):
        """
        Establece la vista de la base de datos a consultar.

        Args:
            table (str): Nombre de la tabla.
        """
        self._table = str(table).strip().lower()
        return self

    def columns(self, *args):
        """
        Establece las columnas que se deben seleccionar en la consulta.

        Args:
            *args: Nombres de las columnas como argumentos variables.
        """
        self._columns = args
        self._columns_string = ','.join(args)
        return self

    def search(self, value=None):
        """
        Establece el valor de búsqueda.

        Args:
            value (str, optional): Valor a buscar.
        """
        self._search = str(value).strip() if value is not None else None
        return self

    def start(self, start: int):
        """
        Establece el índice de inicio de la consulta.

        Args:
            start (int): Índice de inicio.
        """
        self._start = int(start)
        return self

    def limit(self, limit: int):
        """
        Establece el límite de resultados a devolver.

        Args:
            limit (int): Límite de resultados.
        """
        self._limit = int(limit)
        self._end = self._start + self._limit

        if self._limit <= 0:
            raise ValueError("El valor del límite debe ser mayor a 0.")
        return self

    def order(self, column, orientation='ASC'):
        """
        Establece el orden de la consulta.

        Args:
            column (int): Índice de la columna para ordenar.
            orientation (str, optional): Dirección de orden ('ASC' o 'DESC'). Defaults to 'ASC'.
        """
        self._order_column = column
        self._order_direction = str(orientation).upper()
        return self

    def conditions(self):
        """Genera las condiciones de búsqueda."""
        conditionals = []
        if self._search is not None:
            for column in self._columns:
                conditionals.append(f"{column} LIKE '%{self._search}%'")
            self._conditionals = ' OR '.join(conditionals)

    def serverside(self):
        """
        Este metodo indica que la data que se debe retornar al Front debe tener la estructura de una Datatable
        En modelo ServerSide paginado segun la solicitus.
        """

        if self._db == 'oracle':

            if self._search is None:

                if self._query is None:

                    statement = f"""
                        SELECT {self._columns_string}
                        FROM {self._table}
                        ORDER BY {self._order_column} {self._order_direction}
                        OFFSET {self._start} ROWS
                        FETCH NEXT {self._limit} ROWS ONLY
                    """
                    statement_records_total = f"SELECT COUNT(*) AS total FROM {self._table}"

                else:

                    statement = f"""
                        SELECT {self._columns_string}
                        FROM ({self._query})
                        ORDER BY {self._order_column} {self._order_direction}
                        OFFSET {self._start} ROWS
                        FETCH NEXT {self._limit} ROWS ONLY
                    """
                    statement_records_total = f"SELECT COUNT(*) AS total FROM ({self._query}) SUBQUERY"

            else:

                self.conditions()

                if self._query is None:

                    statement = f"""
                        SELECT {self._columns_string}
                        FROM {self._table}
                        WHERE {self._conditionals}
                        ORDER BY {self._order_column} {self._order_direction}
                        OFFSET {self._start} ROWS
                        FETCH NEXT {self._limit} ROWS ONLY
                    """
                    statement_records_total = f"SELECT COUNT(*) AS total FROM {self._table} WHERE {self._conditionals}"

                else:

                    statement = f"""
                        SELECT {self._columns_string}
                        FROM ({self._query})
                        WHERE {self._conditionals}
                        ORDER BY {self._order_column} {self._order_direction}
                        OFFSET {self._start} ROWS
                        FETCH NEXT {self._limit} ROWS ONLY
                    """
                    statement_records_total = f"SELECT COUNT(*) AS total FROM ({self._query}) SUBQUERY WHERE {self._conditionals}"

            draw = self._draw
            records_total = Oracle().select(statement_records_total).first()
            data = Oracle().select(statement).get()

            self._response = {
                'draw': draw,
                'recordsTotal': records_total["TOTAL"],
                'recordsFiltered': records_total["TOTAL"], #len(data),
                'data': data
            }

            return self

    def clientside(self):
        """
        Este metodo indica que la data que se debe retornar al Front debe tener la estructura de una Datatable
        En modelo ClientSide es decir que se retornará toda la data sin paginacion.
        """

        if self._db == 'oracle':

            if self._query is None:

                statement = f"""
                    SELECT {self._columns_string}
                    FROM {self._table}
                    ORDER BY {self._order_column} {self._order_direction}
                """

            else:

                statement = f"""
                    SELECT {self._columns_string}
                    FROM ({self._query})
                    ORDER BY {self._order_column} {self._order_direction}
                """

            data = Oracle().select(statement).get()

            self._response = {
                'data': data
            }

        return self


    def get(self):
        """
        Ejecuta la consulta y retorna los resultados en formato JSON.

        Returns:
            dict: Resultados en formato JSON.
        """

        if self._serverside:
            self.serverside()
        else:
            self.clientside()

        return jsonify(self._response)

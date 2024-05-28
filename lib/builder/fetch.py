from lib.builder.collections import Collection

class Fetch:

    def __init__(self, cursor):
        """Recibe la data de la consulta"""
        self.cursor = cursor

    def headers(self):
        """Retorna solo el nombre de las columnas"""
        return [desc[0] for desc in self.cursor.description]

    def column(self, position:int):
        """Retorna solo los valoresde la columna de acuerdo a su posición"""
        rows = self.cursor.fetchall()

        data = []
        for row in rows:
            data.append(row[position])

        return data

    def rows(self):
        """Retorna solo los valores solo de las filas"""
        return self.cursor.fetchall()

    def fetch(self):
        """Retorna una coleccion de valores indexados"""
        headers_featch = [desc[0] for desc in self.cursor.description]
        rows_featch = [dict(zip(headers_featch, row)) for row in self.cursor.fetchall()]
        return Collection(data=rows_featch)
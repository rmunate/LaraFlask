class Collection:
    """
    Clase que representa una colección de datos.

    Attributes:
        data (list): Los datos almacenados en la colección.
    """

    def __init__(self, data):
        """
        Inicializa una instancia de la clase Collection con los datos proporcionados.

        Args:
            data (list): Los datos a almacenar en la colección.
        """
        self.data = data

    def first(self):
        """
        Devuelve el primer elemento de la colección o None si la colección está vacía.

        Returns:
            any: El primer elemento de la colección o None si está vacía.
        """
        return self.data[0] if self.data else None

    def last(self):
        """
        Devuelve el último elemento de la colección o None si la colección está vacía.

        Returns:
            any: El último elemento de la colección o None si está vacía.
        """
        return self.data[-1] if self.data else None

    def get(self):
        """
        Devuelve todos los datos almacenados en la colección.

        Returns:
            list: Todos los datos almacenados en la colección.
        """
        return self.data

    def chunk(self, size:int):
        """
        Divide la colección en bloques de tamaño especificado.

        Args:
            size (int): El tamaño de cada bloque.

        Returns:
            list: Una lista de listas, donde cada sublista es un bloque de datos.
        """
        if size <= 0:
            raise ValueError("El tamaño de chunk debe ser un entero positivo mayor que cero.")

        return [self.data[i:i + size] for i in range(0, len(self.data), size)]


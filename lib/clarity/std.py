class ObjectCustom:

    """
    Esta clase define un objeto personalizado que permite acceder a atributos
    inexistentes devolviendo None en lugar de generar una excepción AttributeError.
    """
    def __getattr__(self, name):
        return None
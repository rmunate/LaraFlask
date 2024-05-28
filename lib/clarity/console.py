import sys

class Console:
    """
    Esta clase es útil para generar salidas por consola del proyecto.
    Permite generar salidas mejoradas frente a los colores de impresión de los valores.
    También permite generar impresiones por consola y detener la ejecución del sistema.
    """

    # Paleta de Colores
    default = '\033[0m'
    info_color = '\033[34m'
    danger_color = '\033[91m'
    warning_color = '\033[93m'
    success_color = '\033[92m'

    @staticmethod
    def dump(value):
        """
        Imprime el valor en la consola y detiene la ejecución del Script.

        Args:
            value (any): El valor que se imprimirá antes de detener la ejecución.
        """
        print(value)
        sys.exit()

    @staticmethod
    def write(message=''):
        """
        Imprime el valor en la pantalla sin aplicar ningún tipo de estilos.

        Args:
            message (str, optional): El mensaje a imprimir. Por defecto, es una cadena vacía.
        """
        print(f"{Console.default}{message}{Console.default}")

    @staticmethod
    def line(lines=1):
        """
        Imprime saltos de linea.

        Args:
            lines (int, optional): Cantidad de saltos de linea.
        """
        for i in range(lines):
            print("")

    @staticmethod
    def info(message=''):
        """
        Imprime el valor en letras azules determinando un mensaje informativo.

        Args:
            message (str, optional): El mensaje a imprimir. Por defecto, es una cadena vacía.
        """
        print(f"{Console.info_color}{message}{Console.default}")

    @staticmethod
    def danger(message=''):
        """
        Imprime el valor en letras rojas determinando un mensaje de error.

        Args:
            message (str, optional): El mensaje a imprimir. Por defecto, es una cadena vacía.
        """
        print(f"{Console.danger_color}{message}{Console.default}")

    @staticmethod
    def warning(message=''):
        """
        Imprime el valor en letras amarillas determinando un mensaje de alerta.

        Args:
            message (str, optional): El mensaje a imprimir. Por defecto, es una cadena vacía.
        """
        print(f"{Console.warning_color}{message}{Console.default}")

    @staticmethod
    def success(message=''):
        """
        Imprime el valor en letras verdes determinando un mensaje de éxito.

        Args:
            message (str, optional): El mensaje a imprimir. Por defecto, es una cadena vacía.
        """
        print(f"{Console.success_color}{message}{Console.default}")

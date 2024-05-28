import os,shutil
from lib.clarity.paths import Paths

class ControlCache:
    """
    Manejador del __pycache__:
    Clase para eliminar el bytecode al reiniciar el marco
    """

    @staticmethod
    def clear():

        """
        Elimina de manera recursiva todas las carpetas __pycache__ y sus contenidos.
        """

        for root, dirs, files in os.walk(Paths.base()):
            for dir in dirs:
                if dir == '__pycache__':
                    pycache_path = os.path.join(root, dir)
                    shutil.rmtree(pycache_path)

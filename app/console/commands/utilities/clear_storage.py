from lib.clarity.paths import Paths
from lib.clarity.file import File
import datetime
import os

class ClearStorageCommand:

    """
    Este comando se encarga de enviar el informe plano de despachos diariamente a las 04:00am.
    """

    def __init__(self):
        """
        Logica Necesaria para inicializar el Comando
        """

        # Antiguedad maxima en [minutos] para eliminar archivos del Storage
        self.max_time = 10

    def handle(self):

        """
        Logica para eliminar archivos viejos cada vez que se ejecute el JOB
        """

        # Marca de tiempo.
        now = datetime.datetime.now()
        max_life_time = now - datetime.timedelta(minutes=self.max_time)

        # Iterar sobre los archivos en la carpeta
        for name_file in File.list():

            # Obtener El Full Path
            full_path = File.path(name=name_file)

            # Obtener la fecha de creación del archivo
            created_file = datetime.datetime.fromtimestamp(os.path.getctime(full_path))

            # Verificar si la fecha de creación es anterior al tiempo límite
            if created_file < max_life_time:
                File.delete(name=name_file)


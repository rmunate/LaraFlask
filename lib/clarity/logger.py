import os
import logging
from datetime import datetime
from lib.clarity.paths import Paths
from lib.environment.config import Config

class Logger:
    """
    Esta clase se encarga de crear el Log de ejecucion de la aplicacion.
    Esta clase se cargará por defecto en el Kernel de la aplicacion sin embargo
    se podra tambien usar desde donde el usuario lo desee.
    """

    """Alojar La instancia del Logguer"""
    _instance = None

    def __new__(cls):
        """
        Crea una nueva instancia de Logger si no existe una previamente.

        Returns:
            Logger: Una instancia de la clase Logger.
        """
        if not cls._instance:
            cls._instance = super(Logger, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        """
        Inicializa la instancia del Logger.

        Toma el valor del entorno y define el uso del Logger.
        """
        self.mode = Config.app('logger')
        if self.mode:
            InirLocalLogging()

    def start(self, message=None):
        """
        Inicializa el registro del Logger.

        Args:
            message (str, optional): Un mensaje opcional para registrar al inicio. Por defecto, es None.

        Returns:
            bool: True si la inicialización del registro del Logger fue exitosa.
        """
        if self.mode:
            logging.info("-----------------------------------------------------------------")
            if message is not None:
                logging.info(message)
        return True

    def info(self, message):
        """
        Genera un registro informativo en el Log.

        Args:
            message (str): El mensaje informativo a registrar.

        Returns:
            bool: True si la generación del registro informativo fue exitosa.
        """
        if self.mode:
            logging.info(message)
        return True

    def error(self,message):
        """
        Genera un registro de error en el Log.

        Args:
            message (str): El mensaje de error a registrar.

        Returns:
            bool: True si la generación del registro de error fue exitosa.
        """
        if self.mode:
            logging.error(message)
        return True


class InirLocalLogging:

    """
    Esta clase se encarga de manejar un singleton de montaje del Log del sistema.
    """

    """Alojar La instancia del InirLocalLogging"""
    _instance = None

    def __new__(cls):
        """
        Registra una única instancia del Logger.

        Returns:
            InitLocalLogging: Una instancia de la clase InitLocalLogging.
        """
        if not cls._instance:
            cls._instance = super(InirLocalLogging, cls).__new__(cls)
            cls._instance._init_logger()
        return cls._instance

    def _init_logger(self):
        """
        Configura el logging del sistema.
        """
        try:

            # Obtener la fecha actual.
            currentDate = datetime.now()
            dateNameLogFile = currentDate.strftime("%Y_%m_%d")

            # Obtener la ruta del directorio de logs.
            log_directory = os.path.abspath(os.path.join(Paths.base(), "storage","log"))
            os.makedirs(log_directory, exist_ok=True)

            # Definir la ruta del archivo de log.
            log_file_path = os.path.join(log_directory, f"APP_{dateNameLogFile}.log")

            # Configurar el logging con la ruta del archivo de log.
            logging.basicConfig(
                filename=log_file_path,
                level=logging.INFO,
                format='%(asctime)s [%(levelname)s]: %(message)s',
                datefmt='%Y-%m-%d %H:%M:%S',
                encoding='utf-8'
            )

        except Exception as error:

            # Lanzar Excepcion del Error.
            raise ValueError(f"[Log]: Error al inicializar el logger, {error}")
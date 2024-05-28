from dotenv import load_dotenv
import os

class Env:

    """
    Esta clase hace la carga del Entorno del sistema
    Se encarga de leer el archivo (.env) de la raiz del proyecto.
    """

    # Instancia unica del ENV
    _instance = None

    def __new__(cls):
        """
        Carga única del ENV (Singleton).
        """
        if cls._instance is None:
            cls._instance = super(Env, cls).__new__(cls)
            cls._instance._loaded = False
        return cls._instance

    @staticmethod
    def load_env():
        """
        Método para cargar el ENV.
        """
        if not hasattr(Env._instance, '_loaded') or not Env._instance._loaded:
            env_path = os.path.join(os.path.dirname(__file__), '../../.env')
            load_dotenv(env_path)
            Env._instance._loaded = True

    @staticmethod
    def get(key, default=None):
        """
        Método para obtener un valor del ENV.

        Args:
            key (str): La clave del valor que se quiere obtener.
            default (str, optional): El valor predeterminado si la clave no se encuentra. Por defecto, None.

        Returns:
            str: El valor correspondiente a la clave o el valor predeterminado si la clave no se encuentra.
        """
        Env().load_env()
        value = os.getenv(key)
        if value is None:
            return default
        return value

    @staticmethod
    def clear():
        """
        Método para reiniciar el Entorno.
        """
        Env._instance = None

    @staticmethod
    def init():
        """
        Método para reiniciar el Entorno.
        """
        Env._instance = None
        Env()

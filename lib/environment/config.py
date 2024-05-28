import json
import os
from lib.clarity.paths import Paths
from config.database import connections
from config.endpoints import uris
from config.mail import mail
from config.cors import cors
from config.app import app

class Config:

    _instance = None
    _json = None

    def __new__(cls, *args, **kwargs):
        """
        Crea una instancia única de la clase Config utilizando el patrón Singleton.

        Args:
            cls: La clase actual.
            *args: Argumentos posicionales arbitrarios.
            **kwargs: Argumentos de palabras clave arbitrarios.

        Returns:
            Config: La instancia única de la clase Config.
        """

        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        """
            Constructor de la clase para inicializar el atributo 'path' con la ruta al archivo de configuración JSON.
        """

        self.path = os.path.join(Paths.base(), "bootstrap", "cache", "config.json")

    def mount(self):
        """
            Monta un archivo de configuración de variables de entorno en formato JSON si no existe en 'self.path'.
        """
        if not os.path.exists(self.path):

            globalConfigData = json.dumps([{
                "app": app,
                "cors": cors,
                "database": connections,
                "endpoints": uris,
                "mail": mail
            }])

            with open(self.path, 'w') as f:
                f.write(globalConfigData)

        return True

    def destroy(self):
        """
            Elimina el archivo de configuración JSON si existe en la ruta 'self.path'.

            Retorna:
                True si el archivo se eliminó correctamente, False si el archivo no existe.
        """
        if os.path.exists(self.path):
            os.remove(self.path)

            return True
        else:
            return False

    def read(self):
        """
            Lee y carga el contenido del archivo de configuración JSON en la ruta 'self.path'.

            Si el archivo no existe, se crea uno nuevo mediante el método 'mount()'.

            Retorna:
                Un diccionario con los datos cargados desde el archivo JSON.
        """
        self.mount()

        if self._json is None:
            with open(self.path, 'r') as f:
                contenido = f.read()
                self._json = json.loads(contenido)

        return self._json

    def section(self, section:str, value:str):
        """
            Obtiene un valor específico de una sección del archivo de configuración JSON.

            Args:
                section (str): La sección del archivo de configuración.
                value (str): La clave o ruta del valor que se desea obtener dentro de la sección.

            Retorna:
                El valor correspondiente a la clave especificada dentro de la sección, o None si no se encuentra.
        """
        appData = self.read()[0][section]

        if value is not None:
            indexes = value.split('.')
            realData = appData
            try:
                for index in indexes:
                    realData = realData[index]
            except (TypeError, KeyError):
                realData = None
        else:
            realData = appData

        return realData


    @staticmethod
    def app(value:str = None):
        """
            Obtiene un valor específico de la sección 'app' del archivo de configuración JSON.

            Args:
                value (str, opcional): La clave o ruta del valor que se desea obtener dentro de la sección.
                    Si se omite, devuelve toda la sección 'app'.

            Retorna:
                El valor correspondiente a la clave especificada dentro de la sección 'app', o la sección completa si value es None.
        """
        return Config().section(
            section="app",
            value=value
        )

    @staticmethod
    def cors(value:str = None):
        """
            Obtiene un valor específico de la sección 'cors' del archivo de configuración JSON.

            Args:
                value (str, opcional): La clave o ruta del valor que se desea obtener dentro de la sección.
                    Si se omite, devuelve toda la sección 'cors'.

            Retorna:
                El valor correspondiente a la clave especificada dentro de la sección 'cors', o la sección completa si value es None.
        """
        return Config().section(
            section="cors",
            value=value
        )

    @staticmethod
    def database(value:str = None):
        """
            Obtiene un valor específico de la sección 'database' del archivo de configuración JSON.

            Args:
                value (str, opcional): La clave o ruta del valor que se desea obtener dentro de la sección.
                    Si se omite, devuelve toda la sección 'database'.

            Retorna:
                El valor correspondiente a la clave especificada dentro de la sección 'database', o la sección completa si value es None.
        """
        return Config().section(
            section="database",
            value=value
        )

    @staticmethod
    def mail(value:str = None):
        """
            Obtiene un valor específico de la sección 'mail' del archivo de configuración JSON.

            Args:
                value (str, opcional): La clave o ruta del valor que se desea obtener dentro de la sección.
                    Si se omite, devuelve toda la sección 'mail'.

            Retorna:
                El valor correspondiente a la clave especificada dentro de la sección 'mail', o la sección completa si value es None.
        """
        return Config().section(
            section="mail",
            value=value
        )

    @staticmethod
    def endpoints(value:str = None):
        """
            Obtiene un valor específico de la sección 'endpoints' del archivo de configuración JSON.

            Args:
                value (str, opcional): La clave o ruta del valor que se desea obtener dentro de la sección.
                    Si se omite, devuelve toda la sección 'endpoints'.

            Retorna:
                El valor correspondiente a la clave especificada dentro de la sección 'endpoints', o la sección completa si value es None.
        """
        return Config().section(
            section="endpoints",
            value=value
        )
import re, sys, datetime, traceback, importlib
from flask import Flask
from flask_cors import CORS
from lib.environment.env import Env
from lib.clarity.cache import ControlCache
from lib.clarity.paths import Paths
from lib.clarity.logger import Logger
from lib.http.router import BluePrint
from lib.environment.config import Config
from lib.clarity.console import Console
from lib.http.response import JsonResponse

class LaraFlask(Flask):

    def __init__(self, *args, **kwargs):

        # Inicializar Clase.
        super(LaraFlask, self).__init__(*args, **kwargs)

        # Configurar un manejador de errores global para excepciones no controladas
        self.register_error_handler(Exception, self.handle_global_error)

    def handle_global_error(self, e):

        """
        Este metodo encapsula los errores en la ejecucion de Flask

        Returns:
            e: Error Generado En La Instancia de Flask
        """
        error = str(e)
        traceback_list = traceback.format_tb(e.__traceback__)
        last_traceback_line_string = re.sub(r'\s+', ' ', traceback_list[-1].strip().replace('\n', ', '))

        Console.write("----------------------------------")
        Console.warning(f" * Runtime Error - LaraFlask:")
        Console.write("----------------------------------")
        Console.warning(f" * Location : {last_traceback_line_string}")
        Console.write("----------------------------------")
        Console.danger(f" * Exception: {error}")

        Logger().error(
            message=f"Location: {last_traceback_line_string}"
        )

        Logger().error(
            message=f"Exception: {error}"
        )

        return JsonResponse.serverError(
            message={
                "location":last_traceback_line_string,
                "error":error
            }
        )

class HttpKernel:
    """
    Clase para manejar el kernel HTTP de la aplicación.
    """

    _instance = None

    def __new__(cls, *args, **kwargs):
        """
        Crea una instancia única de la clase HttpKernel utilizando el patrón Singleton.

        Args:
            cls: La clase actual.
            *args: Argumentos posicionales arbitrarios.
            **kwargs: Argumentos de palabras clave arbitrarios.

        Returns:
            HttpKernel: La instancia única de la clase HttpKernel.
        """
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, bytecode=True, debug=None, logger=None):
        """
        Inicializa una instancia de la clase HttpKernel.

        Args:
            bytecode (bool): Indica si se emplea el bytecode.
            debug (bool): Indica si se emplea el modo debug.
            logger (bool): Indica si se emplea el logger.
        """

        # Vaciar Cache
        ControlCache.clear()
        Config().destroy()

        # Cargar el ENV
        Env.init()

        # crear Cache de Configuracion.
        Config().mount()

        # Iniciar app de flask
        self.app = LaraFlask(__name__)

        # Definir carpeta de sesoion
        self.app.config['SESSION_FILE_DIR'] = Paths.session()

        # Definir si se emplea bytecode
        sys.dont_write_bytecode = bytecode

        # Definir si se emplea debug a la app
        self.debug = Config.app("debug") if debug is None else debug

        # Definir si se emplea log a la app
        self.logger = Config.app("logger") if logger is None else logger

        # Aplicar configuracion de CORS App
        CORS(
            app=self.app,
            methods=Config.cors('allowed_methods'),
            origins=Config.cors('allowed_origins'),
            allow_headers=Config.cors('allowed_headers'),
            expose_headers=Config.cors('exposed_headers'),
            max_age=Config.cors('max_age')
        )

        # Ejecutar la creacion de las Rutas
        importlib.import_module('routes.api')

        # Marce de Log
        if self.logger:

            now = datetime.datetime.now().date()
            starTimestamp = now.strftime('%Y-%m-%d %H:%M:%S')

            Logger().start(
                message=f"Inicio de Ejecución. {starTimestamp}"
            )

    def blueprint(self):
        """
        Monta las rutas definidas para el sistema en la subinstancia de Flask.

        Returns:
            Retorna La instancia de la aplicación Flask.
        """

        app = BluePrint(app=self.app, logger=self.logger).routes()
        return app

class Bootstrap:

    @staticmethod
    def app(instance_flask):

        """
        Inicializa una instancia de la clase HttpKernel.

        Args:
            bytecode (bool): Indica si se emplea el bytecode.
            debug (bool): Indica si se emplea el modo debug.
            logger (bool): Indica si se emplea el logger.
        """

        try:

            debug = Config.app('debug')

            if debug:
                Console.info(" * LaraFlask v1.0.0")
                Console.success(" * How to develop in Laravel but with Python")

            return instance_flask

        except Exception as error:

            return JsonResponse.serverError(
                message=str(error)
            )
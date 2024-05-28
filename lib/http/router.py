import os
import json
import inspect
import importlib
from flask import request
from lib.clarity.paths import Paths
from lib.clarity.mount import Mount

class Route:
    """
    Clase para manejar la definición dinámica de rutas en una aplicación Flask.
    """

    _instance = None
    _middleware = None
    _base = None
    _prefix = None

    def __new__(cls, *args, **kwargs):
        """
        Crea una nueva instancia de la clase Route si aún no existe, utilizando el patrón Singleton.

        Args:
            cls: La clase actual.
            *args: Argumentos posicionales arbitrarios.
            **kwargs: Argumentos de palabras clave arbitrarios.

        Returns:
            La instancia única de la clase Route.
        """
        if not cls._instance:
            Router().clear()
            cls._instance = super().__new__(cls)
        cls._instance._middleware = None
        cls._instance._base = None
        cls._instance._prefix = None
        return cls._instance

    def __init__(self, base=None):
        """
        Inicializa una instancia de la clase Route.

        Args:
            middleware: El middleware opcional que se aplicará a las rutas definidas con esta instancia de Route.
            base: El grupo general de las rutas, comunemente se usa para que todas las rutas antes de su prefix inician con [api/].
            prefix: El prefijo opcional que se aplicará a las URIs de las rutas definidas con esta instancia de Route.
        """
        self._base = base

    def middleware(self, instance):
        """
        Determina que la ruta debe pasar previamente por un middleware antes de llegar al controlador.

        Args:
            instance: El middleware opcional que se aplicará a las rutas definidas con esta instancia de Route.
        """
        self._middleware = instance
        return self

    def prefix(self, prefix):
        """
        Determina que la ruta debe pasar previamente por un middleware antes de llegar al controlador.

        Args:
            prefix: El prefijo opcional que se aplicará a las URIs de las rutas definidas con esta instancia de Route.
        """
        self._prefix = prefix
        return self

    def group(self, *args):
        """
            Inicializa el manejador de rutas con las rutas especificadas.
            Limpia todas las rutas existentes y luego agrega las rutas proporcionadas como argumentos.
            Args:
                *args (str): Una lista de rutas a agregar al manejador de rutas.
        """
        for route in args:

            if self._middleware is not None:
                # Agrega información del middleware a las rutas si está presente
                route["middleware_file"] = inspect.getmodule(self._middleware).__name__
                route["middleware_class"] = self._middleware.__name__
                route["middleware_method"] = 'handle'

            if self._prefix is not None:
                # Agrega un prefijo a las URIs de las rutas si está presente
                route["uri"] = str("/" + self._prefix + "/" + route["uri"])

            if self._base is not None:
                # Agrega la base del ruteador
                route["uri"] = str("/" + self._base + "/" + route["uri"])

            # Saneamiento de Ruta
            route["uri"] = str("/" + route["uri"]).replace('//','/')

            # Agrega la ruta al manejador de rutas
            Router().set(route)

    @staticmethod
    def post(url:str, controller:dict):
        """
            Define una ruta POST en el manejador de rutas.
            Args:
                ruta (str): La ruta de la solicitud POST.
                controller (dict): Un diccionario que contiene el controlador para la ruta POST, con la estructura (clase, método).
            Returns:
                dict: Un diccionario que describe la ruta POST, incluyendo el verbo HTTP, la URI, el módulo, la clase y el método controlador asociado.
        """
        classname, method = controller

        data = {
            "verb": "POST",
            "uri": url,
            "file": inspect.getmodule(classname).__name__,
            "class": classname.__name__,
            "method": method
        }

        return data

    @staticmethod
    def get(url:str, controller:dict):
        """
            Define una ruta GET en el manejador de rutas.
            Args:
                ruta (str): La ruta de la solicitud GET.
                controller (dict): Un diccionario que contiene el controlador para la ruta GET, con la estructura (clase, método).
            Returns:
                dict: Un diccionario que describe la ruta GET, incluyendo el verbo HTTP, la URI, el módulo, la clase y el método controlador asociado.
        """
        classname, method = controller

        data = {
            "verb": "GET",
            "uri": url,
            "file": inspect.getmodule(classname).__name__,
            "class": classname.__name__,
            "method": method
        }

        return data

class Router:
    """
    Clase para manejar las rutas de la aplicación.

    Attributes:
        path (str): La ruta del archivo de rutas.
    """

    """Alojar La instancia del Logguer"""
    _instance = None

    def __new__(cls):
        """
        Crea una nueva instancia de Router si no existe una previamente.

        Returns:
            Router: Una instancia de la clase Router.
        """

        if not cls._instance:
            cls._instance = super(Router, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        """
            Inicializa la clase Router.
        """

        self.path = os.path.join(Paths.base(), "bootstrap", "cache", "route.json")

    def clear(self):
        """
            Borra el archivo de ruta si existe.
        """
        if os.path.exists(self.path):
            os.remove(self.path)

    def validate(self, path, classname, method):
        """
            Valida si la clase y el método especificados existen en el módulo dado.
            Args:
                path (str): La ruta del módulo.
                classname (str): El nombre de la clase.
                method (str): El nombre del método.
            Raises:
                ValueError: Si el método no existe en la clase o si hay errores durante la importación o la búsqueda.
        """
        try:
            # Importar dinámicamente el módulo
            module = importlib.import_module(path)

            # Obtener la clase del módulo
            class_obj = getattr(module, classname)

            # Verificar si la clase tiene el método requerido
            if hasattr(class_obj, method) and callable(getattr(class_obj, method)):
                exist = True
            else:
                exist = False

        except (ImportError, AttributeError) as e:
            exist = False

        if not exist:
            self.clear()
            raise ValueError(f"No se encontró el metodo '{method}' dentro de la clase '{classname}' en el archivo '{path}'")


    def uniqueUri(self, currentData, newData):
        """
            Verifica si una nueva ruta tiene una URI única dentro de las rutas existentes.
            Args:
                currentData (list): La lista de datos de rutas existentes.
                newData (dict): Los datos de la nueva ruta que se está agregando.
            Returns:
                bool: True si la URI de la nueva ruta es única, False de lo contrario.
            Raises:
                ValueError: Si se intenta agregar una ruta con la misma URI y el mismo verbo que una ruta existente.
        """
        for route in currentData:

            verb = route["verb"]
            uri = route["uri"]

            if newData["verb"] == verb and newData["uri"] == uri:
                self.clear()
                raise ValueError(f"No pueden existir dos rutas con el mismo verbo y la misma uri, [{verb}] - [{uri}]")

        return True

    def set(self, data):
        """
            Agrega una nueva ruta al archivo de rutas.
            Args:
                data (dict): Un diccionario que contiene los datos de la nueva ruta, incluyendo el módulo, la clase y el método.
            Raises:
                ValueError: Si la clase o el método especificados no existen, o si la ruta y el verbo ya están en uso.
        """
        # Extraer Valores
        file = data["file"]
        classname = data["class"]
        method = data["method"]
        middleware_file = data["middleware_file"] if 'middleware_file' in data else None
        middleware_classname= data["middleware_class"] if 'middleware_class' in data else None
        middleware_method= data["middleware_method"] if 'middleware_method' in data else None

        # Validar que existan las clases y los metodos tanto del Controlador como del Middleware.
        self.validate(path=file, classname=classname, method=method)

        if middleware_file is not None:
            self.validate(path=middleware_file, classname=middleware_classname, method=middleware_method)

        # Extraer Contenido Actual
        contenido = []
        if os.path.exists(self.path):
            with open(self.path, 'r') as f:
                contenido = f.read()
            contenido = json.loads(contenido)

        # Validar que no exista esta ruta y este vervbo en uso
        self.uniqueUri(
            currentData=contenido,
            newData=data
        )

        # Agregar Nuevo contenido
        contenido.append(data)
        with open(self.path, 'w') as f:
            f.write(json.dumps(contenido))

class BluePrint:
    """
    Clase para configurar las rutas en una aplicación.
    """

    def __init__(self, app, logger):
        """
        Inicializa una instancia de la clase BluePrint.

        Args:
            app: La aplicación Flask a la que se agregarán las rutas.
            logger: El objeto logger para registrar mensajes.
        """
        self.app = app
        self.logger = logger
        self.path = Router().path

    def routes(self):
        """
        Configura las rutas en la aplicación Flask.

        Lee los datos de las rutas desde el archivo de rutas y las registra en la aplicación Flask.

        Returns:
            La instancia de la aplicación Flask después de registrar todas las rutas.
        """
        # Inicializa una lista para almacenar los datos de las rutas
        routes_data = []
        # Verifica si existe el archivo de rutas
        if os.path.exists(self.path):
            # Lee los datos de las rutas desde el archivo de rutas
            with open(self.path, 'r') as f:
                routes_data = json.load(f)

        # Itera sobre los datos de las rutas
        for i, route_data in enumerate(routes_data):

            # Extrae los datos de la ruta
            verb = route_data["verb"]
            uri = route_data["uri"]
            method_name = route_data["method"]
            class_name = route_data["class"]

            # Data Controlador
            next_controller = {
                "path" : route_data["file"],
                "classname" : route_data["class"],
                "method" : route_data["method"]
            }

            if 'middleware_file' in route_data and route_data["middleware_file"] is not None:
                # Si hay un middleware, extrae sus datos
                next_middleware = {
                    "path" : route_data["middleware_file"],
                    "classname" : route_data["middleware_class"],
                    "method" : route_data["middleware_method"],
                }
                # Llama al middleware y obtiene el método a llamar
                method_to_call = Mount.middleware(
                    next=next_middleware,
                    data_controller=next_controller,
                    flask_request=request
                )
            else:
                # Si no hay middleware, llama directamente al controlador
                method_to_call = Mount.controller(
                    next=next_controller,
                    flask_request=request
                )

            # Registrar la ruta en Flask según el verbo HTTP
            self.app.add_url_rule(
                rule=uri,
                endpoint=str(uri).replace("/","_"),
                view_func=method_to_call,
                methods=[verb],
            )

        # Retornar la instancia de Flask después de registrar todas las rutas
        return self.app

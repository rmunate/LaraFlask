from lib.clarity.console import Console
from lib.http.validatator import Validate
import datetime

class Mount:
    """
    Clase para montar middleware y controladores en la aplicación Flask.
    """

    @staticmethod
    def command(instance):

        classname = type(instance).__name__

        # Obtener la marca de tiempo actual.
        current_datetime = datetime.datetime.now()
        start_datetime_str = current_datetime.strftime('%Y-%m-%d %H:%M:%S')

        # Ejecutar el método.
        try:
            instance.handle()
            execution_status = "Success"
        except Exception as e:
            execution_status = f"Error: {str(e)}"

        # Marca de Tiempo de Fin de Ejecución.
        end_datetime = datetime.datetime.now()
        end_datetime_str = end_datetime.strftime('%Y-%m-%d %H:%M:%S')

        # Calcular la duración de la ejecución en segundos.
        execution_duration = (end_datetime - current_datetime).total_seconds()

        # Imprimir el resultado de manera organizada en la consola.
        Console.write("=============================================================")
        Console.info(f"Command: {classname}")
        Console.write("=============================================================")
        if execution_status == "Success":
            Console.success(f"Execution Status Success: {execution_status}")
        else:
            Console.danger(f"Execution Status Fail: {execution_status}")
        Console.info(f"Start Time: {start_datetime_str} | End Time: {end_datetime_str} | Duration: {execution_duration:.2f} seconds")
        Console.write("=============================================================")

    @staticmethod
    def middleware(next, flask_request, data_controller):
        """
        Método estático para montar middleware en la aplicación Flask.

        Args:
            next (dict): Un diccionario que contiene los datos del middleware, incluyendo la ruta, la clase y el método.
            flask_request: La solicitud Flask actual.
            data_controller: Los datos del controlador asociado al middleware.

        Returns:
            Método: El método del middleware a ser llamado.
        """

       # Extraer datos
        path = next["path"]
        classname = next["classname"]
        method = next["method"]

        # Importar el módulo que contiene la clase del middleware
        module = __import__(path, fromlist=[classname])
        new_class = getattr(module, classname)

        # Obtener una instancia del middleware
        middleware_instance = new_class()

        # Agregar Propiedades dinamicas
        middleware_instance.request = flask_request
        middleware_instance.next = data_controller

        # Obtener el método del middleware por nombre
        return getattr(middleware_instance, method)

    @staticmethod
    def controller(next, flask_request, arguments=None):
        """
        Método estático para montar controladores en la aplicación Flask.

        Args:
            next (dict): Un diccionario que contiene los datos del controlador, incluyendo la ruta, la clase y el método.
            flask_request: La solicitud Flask actual.
            arguments (dict): Argumentos adicionales para el método del controlador (opcional).

        Returns:
            Método: El método del controlador a ser llamado.
        """

        # Extraer datos
        path = next["path"]
        classname = next["classname"]
        method = next["method"]

        # Importar el módulo que contiene la clase del controller
        module = __import__(path, fromlist=[classname])
        new_class = getattr(module, classname)

        # Obtener una instancia del controller
        controller_instance = new_class()

        # Agregar Propiedades dinamicas
        controller_instance.request = flask_request
        controller_instance.validate = lambda instance : Validate(flask_request).required(instance.required()).messages(instance.messages()).check()

        # Llamar al método del controlador con argumentos si están presentes, de lo contrario, sin argumentos
        if arguments is not None and len(arguments) > 0:
            return getattr(controller_instance, method)(**arguments)
        elif arguments is not None and len(arguments) == 0:
            return getattr(controller_instance, method)()
        elif arguments is None:
            return getattr(controller_instance, method)
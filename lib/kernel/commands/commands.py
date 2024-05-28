from lib.clarity.mount import Mount
import json

class ExecuteCommand:

    """
    Comando para inicializar los Demons.
    """

    def handler(self, path, classname, params, custom=True):

        """
        Manejador del comando
        """

        # Extraer datos
        path = str(path).replace("/", ".").replace("\\",".")

        # En caso de que sea un comando personalizado.
        if custom:
            path = f"app.console.commands.{path}"

        # Importar el módulo que contiene la clase del middleware
        module = __import__(path, fromlist=[classname])
        new_class = getattr(module, classname)

        # Ejecutar la carga de las tareas
        if params is None or len(params) == 0:
            Mount.command(new_class())
        else:
            params = json.loads(str(params).replace("'",'"').strip())
            Mount.command(new_class(**params))

import importlib
from app.console.kernel import Kernel
from lib.clarity.cache import ControlCache
from lib.environment.config import Config
from lib.environment.env import Env
from lib.win64.tasks import WindowsScheduler

class RegenerateCacheCommand:

    """
    Comando para regenerar el cache del Sistema.
    """

    def handle(self):

        """
        Manejador del comando
        """

        # Vaciar Cache
        Config().destroy()

        # Cargar el ENV
        Env.init()

        # Crear Nuevamente El Cache de Configuracion.
        Config().mount()

        # Ejecutar la creacion de las Rutas
        importlib.import_module('routes.api')

        # Eliminar Recursivamente Bytecode
        ControlCache.clear()


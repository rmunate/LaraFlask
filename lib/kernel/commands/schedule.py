from app.console.kernel import Kernel
from lib.win64.tasks import WindowsScheduler

class ScheduleCommand:

    """
    Comando para inicializar los Demons.
    """

    def handler(self):

        """
        Manejador del comando
        """

        # Ejecutar la carga de las tareas
        Kernel().schedule()

        # Validar que haya Ejecuciones
        if len(WindowsScheduler.getAll()) > 0:
            WindowsScheduler.run()

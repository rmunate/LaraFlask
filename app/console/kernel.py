from app.console.commands.utilities.clear_storage import ClearStorageCommand
from lib.win64.tasks import WindowsScheduler
from lib.clarity.mount import Mount

class Kernel:

    """
    Este clase se encarga de administrar la ejecucion de los comandos.
    El metodo (schedule) permite definir como se denejan ejecutar las tareas a nivel de sistema Operativo.
    """

    def schedule(self):

        WindowsScheduler.every().hour.at(":00").do(lambda: Mount.command(ClearStorageCommand()))


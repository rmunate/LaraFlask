import schedule
import time

class WindowsScheduler:
    """
    Esta clase proporciona métodos para programar tareas en Windows.
    Es un envoltorio (Wrapper) para la biblioteca 'schedule', diseñado para ofrecer una interfaz de usuario más amigable.
    """

    @staticmethod
    def every(value:int=None):
        """
        Define la frecuencia con la que se desea ejecutar una tarea.

        Args:
            value (int): El valor que representa la frecuencia de ejecución de la tarea.

        Returns:
            Job: Un objeto Job de la biblioteca 'schedule' que permite configurar la tarea.
        """
        singletonSchedule = schedule
        if value is not None:
            return singletonSchedule.every(value)
        else:
            return singletonSchedule.every()

    @staticmethod
    def run():
        """
        Inicia la ejecución del script.

        Este método ejecuta todas las tareas programadas y se mantiene en un bucle continuo hasta que se interrumpe.
        """
        while True:
            schedule.run_pending()
            time.sleep(1)

    @staticmethod
    def getAll():
        """
        Obtiene una lista de todas las tareas programadas.

        Returns:
            list: Una lista de objetos Job que representan las tareas programadas.
        """
        return schedule.get_jobs()

    # Limpiart Los Jobs
    @staticmethod
    def clear():
        """
        Elimina todas las tareas programadas.

        Returns:
            int: El número de tareas eliminadas.
        """
        return schedule.clear()

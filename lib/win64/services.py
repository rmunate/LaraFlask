import win32serviceutil
import time

class ServicesRestart:
    """
    Esta clase proporciona métodos para controlar y reiniciar servicios en Windows.
    """

    @staticmethod
    def is_running(service):
        """
        Determina si un servicio está en ejecución en Windows.

        Args:
            service (str): El nombre del servicio a verificar.

        Returns:
            bool: True si el servicio está en ejecución, False de lo contrario.
        """
        try:
            # Consultar el estado del servicio de impresión
            service_status = win32serviceutil.QueryServiceStatus(service)[1]

            # Verificar si el servicio está en ejecución
            return service_status in [4,5,6,7]

        except Exception as e:

            # Informar que no se encuentra activo el servicio.
            return False

    def __init__(self, name:str):
        """
        Inicializa la clase ServicesRestart con el nombre del servicio.

        Args:
            name (str): El nombre del servicio a reiniciar.
        """
        self.name = name
        self.sleep = 7

    def delay(self, seconds):
        """
        Establece el tiempo de espera entre peticiones de reinicio del servicio.

        Args:
            seconds (int): El tiempo de espera en segundos.

        Returns:
            ServicesRestart: La instancia de la clase ServicesRestart.
        """
        if seconds > 7:
            self.sleep = seconds
        return self

    def execute(self):
        """
        Ejecuta la acción de reiniciar el servicio.

        Returns:
            bool: True si el reinicio del servicio fue exitoso, False de lo contrario.
        """
        try:

            # Verificar si el servicio está en ejecución
            if ServicesRestart.is_running(service=self.name):

                # Detener el servicio
                win32serviceutil.StopService(self.name)

                # Esperar a que se detenga
                time.sleep(self.sleep)

            # Iniciar el servicio
            win32serviceutil.StartService(self.name)

            # Esperar a que se inicie
            time.sleep(self.sleep)

            # Bandera de Exito
            return True

        except Exception as e:

            # Informar que no se encuentra activo el servicio.
            return False
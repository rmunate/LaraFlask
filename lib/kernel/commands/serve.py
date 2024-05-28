import os
import time

class ServeCommand:

    """
    Comando para inicializar el servidor de desarrollo.
    """

    def handler(self, debug, use_reloader, host, port):

        """
        Manejador del comando
        """
        self.elegant_loading()
        self.clear_console()

        from bootstrap.app import laraflask
        laraflask.run(
            debug=debug,
            use_reloader=use_reloader,
            host=host,
            port=port,
            threaded=True
        )

    def clear_console(self):

        """Función para limpiar la consola según el sistema operativo."""

        if os.name == 'posix':
            # Comando para limpiar en sistemas Unix (Linux, macOS)
            _ = os.system('clear')
        elif os.name == 'nt':
            # Comando para limpiar en Windows
            _ = os.system('cls')

    def elegant_loading(self):

        """Función para mostrar una barra de carga elegante."""

        self.clear_console()
        total_iterations = 100
        bar_width = 50

        for i in range(1, total_iterations + 1):
            progress = i / total_iterations
            bar_length = int(bar_width * progress)
            bar = '=' * bar_length + '-' * (bar_width - bar_length)

            # Construir el mensaje de la barra de carga
            loading_message = f"[{bar}] {int(progress * 100)}%"

            # Imprimir la barra de carga
            print(loading_message, end='\r')

            # Simular un pequeño retraso para visualizar el progreso
            time.sleep(0.001)

        print()

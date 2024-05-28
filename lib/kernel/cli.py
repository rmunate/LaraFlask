import argparse
from lib.kernel.commands.cache import RegenerateCacheCommand
from lib.kernel.commands.serve import ServeCommand
from lib.kernel.commands.schedule import ScheduleCommand
from lib.kernel.commands.commands import ExecuteCommand

class CliKernel:

    """
    Kernel para el manejo de las solicitudesd desde el interprete de comandos
    """

    _cli_args = None

    def __init__(self, input):
        parser = argparse.ArgumentParser(description='CLI Kernel Parser')
        parser.add_argument('command', help='Command to execute')
        parser.add_argument('--no-debug', action='store_false', help='Habilitar modo en subprocesos')
        parser.add_argument('--no-reload', action='store_false', help='Habilitar modo en subprocesos')
        parser.add_argument('--host', help='Direccion sobre la cual se ejecutará', default='127.0.0.1')
        parser.add_argument('--port', help='Puerto de Salida', default='5000')
        parser.add_argument('--path', help='Ubicacion del archivo')
        parser.add_argument('--classname', help='Nombre de la clase a ejecutar')
        parser.add_argument('--params', default=None, help='Diccionario para pasar al constructor del commando')
        self._cli_args = parser.parse_args(input[1:])

    def run(self):

        command = self._cli_args.command

        if command == 'serve':

            # Iniciar El Servidor De Desarrollo Del Marco.
            ServeCommand().handler(
                debug=self._cli_args.no_debug,
                use_reloader=self._cli_args.no_reload,
                host=self._cli_args.host,
                port=self._cli_args.port
            )

        elif command == 'schedule':

            # Monta Todos Los Trabajos Programados En Ejecución.
            ScheduleCommand().handler()

        elif command == 'command':

            # Ejecuta Un Comando Personalizado Del Usuario.
            ExecuteCommand().handler(
                path=self._cli_args.path,
                classname=self._cli_args.classname,
                params=self._cli_args.params
            )

        elif command == 'cache:clear':

            # Ejecuta Comando Propio Del Marco.
            ExecuteCommand().handler(
                path='lib.kernel.commands.cache',
                classname='RegenerateCacheCommand',
                params=None,
                custom=False
            )

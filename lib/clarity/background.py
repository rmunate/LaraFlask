import subprocess
from lib.clarity.paths import Paths
import json
import time

class BackgroundCommand:

    @staticmethod
    def execute(path, classname, params, timeout=0):

        # Definir el Path del proyecto
        base_root = Paths.base('artisan')

        # Convertir el diccionario a una cadena JSON con comillas simples
        json_string = json.dumps(params, indent=4, separators=(',', ': '), ensure_ascii=False)

        # Reemplazar las comillas dobles con comillas simples en la cadena JSON
        json_string_single_quotes = json_string.replace('"', "'")

        # Crear Estrcutura e Comandos
        comando = f"python {base_root} command --path=\"{path}\" --classname=\"{classname}\" --params=\"{json_string_single_quotes}\""

        # Iniciar proceso en Segundo Pladno
        subprocess.Popen(comando, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        # Dormir
        time.sleep(timeout)
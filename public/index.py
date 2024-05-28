import os
import sys

#--------------------------------------------------------------------------
# Folders de la solución
#--------------------------------------------------------------------------
#
# En esta seccion se deben encontrar las carpetas que harán parte integral
# de la solucion, por defecto se encuentran las carpetas del Esqueleto
# default de Laraflask
#
#--------------------------------------------------------------------------
paths = [
    'app',
    'bootstrap',
    'config',
    'public',
    'routes',
    'resources',
    'storage',
    'tests',
    'src'
]

#--------------------------------------------------------------------------
# Registar Paths
#--------------------------------------------------------------------------
#
# En esta seccion registraremos los archivos de nuestra solicion en el
# BasePath de este proyecto.
#
#--------------------------------------------------------------------------
basepath = os.path.join(os.path.abspath(os.path.dirname(__file__)), '../')

if basepath not in sys.path:
    sys.path.append(basepath)

for folder in paths:
    for root, dirs, files in os.walk(os.path.join(basepath, folder)):
        if root not in sys.path:
            sys.path.append(root)

#--------------------------------------------------------------------------
# Obtener Instancia de la Aplicacion
#--------------------------------------------------------------------------
#
# Llamaremos la instancia de nuestra aplicacion LAraFlask (Wrapper Flask)
# Esta nos permirá aplicar el Handler de inicio de servicios.
#
#--------------------------------------------------------------------------
from bootstrap.app import laraflask

app = laraflask

#--------------------------------------------------------------------------
# Ejecutar la Aplicación
#--------------------------------------------------------------------------
#
# Una vez que tenemos la aplicación, podemos manejar la solicitud entrante
# utilizando el kernel HTTP de la aplicación. Luego, enviaremos la respuesta de vuelta
# al navegador de este cliente, permitiéndoles disfrutar de nuestra aplicación.
#
#--------------------------------------------------------------------------
def wsgi_handler(environ, start_response):
    return app(environ, start_response)

if __name__ == '__main__':
    app.run(debug=False, use_reloader=False)
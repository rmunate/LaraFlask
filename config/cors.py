# ------------------------------------------------------------------#
# Configuracion de los Cors Del Sistema.                            #
# ------------------------------------------------------------------#
# Este archivo carga las variables de entorno que se encuentren     #
# disponibles en el archivo .env y las mantiene estaticas para      #
# el tiempo de ejecucion completo de la aplicacion.                 #
# ------------------------------------------------------------------#
from lib.environment.env import Env

cors = {

    'allowed_methods' : ['GET', 'HEAD', 'POST', 'OPTIONS', 'PUT', 'PATCH', 'DELETE'],

    'allowed_origins' : '*',

    'allowed_headers' : '*',

    'exposed_headers' : None,

    'max_age' : None,

}
# ------------------------------------------------------------------#
# Configuracion de los accesos a base de datos.                     #
# ------------------------------------------------------------------#
# Este archivo carga las variables de entorno que se encuentren     #
# disponibles en el archivo .env y las mantiene estaticas para      #
# el tiempo de ejecucion completo de la aplicacion.                 #
# ------------------------------------------------------------------#

from lib.environment.env import Env

connections = {

    'oracle': {
        'default' : {
            "username" : Env.get("DB_SIGWARE_USERNAME"),
            "password" : Env.get("DB_SIGWARE_PASSWORD"),
            "host" : Env.get("DB_SIGWARE_HOST"),
            "service" : Env.get("DB_SIGWARE_SERVICE")
        }
    },
    'sqlserver' : {
        'default' : {
            "username" : Env.get("DB_PTL_USERNAME_PTL"),
            "password" : Env.get("DB_PTL_PASSWORD_PTL"),
            "host" : Env.get("DB_PTL_HOST_PTL"),
            "database" : Env.get("DB_PTL_DATABASE_PTL"),
            "port" : 1433
        },
    }
}
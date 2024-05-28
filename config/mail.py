# ------------------------------------------------------------------#
# Configuracion de la cuenta de correo del sistema                  #
# ------------------------------------------------------------------#
# Este archivo carga las variables de entorno que se encuentren     #
# disponibles en el archivo .env y las mantiene estaticas para      #
# el tiempo de ejecucion completo de la aplicacion.                 #
# ------------------------------------------------------------------#

from lib.environment.env import Env

mail = {

    'default' : {

        # Host del servicio de correo.
        'host': Env.get("MAIL_HOST"),

        # Host del servicio de correo.
        'port': Env.get("MAIL_PORT"),

        # Host del servicio de correo.
        'username': Env.get("MAIL_USERNAME"),

        # Host del servicio de correo.
        'password': Env.get("MAIL_PASSWORD"),

        # Host del servicio de correo.
        'address': Env.get("MAIL_FROM_ADDRESS")

    }

}
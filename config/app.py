# ------------------------------------------------------------------#
# Carga de Configuracion Global de la Aplicacion                    #
# ------------------------------------------------------------------#
# Este archivo carga las variables de entorno que se encuentren     #
# disponibles en el archivo .env y las mantiene estaticas para      #
# el tiempo de ejecucion completo de la aplicacion.                 #
# ------------------------------------------------------------------#
from lib.environment.env import Env

app = {

    #Nombre de la aplicacion
    'name': Env.get("APP_NAME"),

    # Llave privada app.
    'key' : Env.get("APP_KEY"),

    #Environmente
    'environment' : Env.get("APP_ENVIRONMENT"),

    # Define si se debuguea
    'debug' : bool(Env.get("APP_DEBUG", True)),

    # Version de la aplicacion
    'version' : Env.get("APP_VERSION", "1.0.0"),

    # Definir si se creará log de ejecucion
    'logger' : bool(Env.get("APP_LOGGER", True)),

}
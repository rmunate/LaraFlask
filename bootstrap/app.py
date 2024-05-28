#--------------------------------------------------------------------------
# Crear Aplicación
#--------------------------------------------------------------------------
#
# Lo primero que haremos será crear una nueva instancia de la aplicación
# LaraFlask que sirve como "pegamento" para todos los componentes de LaraFlask,
# y es el contenedor del sistema en todas las partes.
#
#--------------------------------------------------------------------------
from lib.kernel.app import HttpKernel, Bootstrap

laraflask = Bootstrap.app(
    HttpKernel(bytecode=True).blueprint()
)
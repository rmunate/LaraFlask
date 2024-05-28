from lib.clarity.std import ObjectCustom

class Validate:
    """
    Esta clase proporciona métodos para validar los datos recibidos en una solicitud HTTP.
    Permite verificar la presencia de campos obligatorios, validar si la solicitud es JSON
    o un diccionario, y generar mensajes de error personalizados en caso de que falle la validación.
    """

    def __init__(self, request):
        """
        Inicializa la clase de validación.

        Args:
            request (request): La solicitud HTTP recibida.
        """
        self.errors = []
        self.request = request
        self.json = False
        self.dict = False

    def required(self, inputs=[]):
        """
        Define los campos obligatorios que deben estar presentes en la solicitud.

        Args:
            inputs (list): Lista de nombres de campos obligatorios.

        Returns:
            Validate: La instancia de la clase Validate.
        """
        self.inputs = inputs
        return self

    def messages(self, messages={}):
        """
        Define mensajes de error personalizados para campos específicos.

        Args:
            messages (dict): Un diccionario que mapea nombres de campos a mensajes de error personalizados.

        Returns:
            Validate: La instancia de la clase Validate.
        """
        self.customMessages = messages
        return self

    def check(self):
        """
        Realiza la validación de la solicitud recibida.

        Returns:
            ObjectCustom: Un objeto personalizado que indica si la validación fue exitosa y
                          contiene una lista de errores si la validación falló.
        """
        # Crear Respuesta.
        resp = ObjectCustom()
        resp.is_valid = True
        resp.errors = self.errors

        # Validar que sea JSON.
        if self.request.method == 'POST':

            if not self.request.is_json:

                self.errors.append('El valor recibido no es un JSON válido.')

                # Crear Respuesta.
                resp.is_valid = False
                resp.errors = ','.join(self.errors)

                # Retorno de Resultado.
                return resp

            else:

                # Extraer Datos del JSON
                data = self.request.get_json()

        elif self.request.method == 'GET':

            # Consultar Argumentos.
            data = self.request.args.to_dict()

        # Validar los campos requeridos.
        for input in self.inputs:

            if input not in data:

                if input in self.customMessages:
                    error = self.customMessages[input]
                else:
                    error = Validate.defultErrorMessage(input)

                self.errors.append(error)

                # Crear Respuesta.
                resp.is_valid = False
                resp.errors = ','.join(self.errors)

                # Retorno de Resultado.
                return resp

        # Retorno de Resultado.
        return resp

    @staticmethod
    def defultErrorMessage(input):
        """
        Genera un mensaje de error predeterminado para un campo requerido no encontrado.

        Args:
            input (str): El nombre del campo requerido.

        Returns:
            str: El mensaje de error predeterminado.
        """
        return f"Se requiere el valor {input} en la solicitud."

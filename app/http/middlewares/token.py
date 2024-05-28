from lib.http.response import JsonResponse
from lib.clarity.mount import Mount

class TokenMiddleware:

    """
    Middleware para garantizar que el usuario se encuentre solicitando la data con un Token Valido.
    Para las conexiones genericas se hará a traves de (Bearer Token), y para las solicitudes de
    alta demanda se hará por X-Api-Key para evitar consumo de base de datos.
    """

    def handle(self, **kwargs):

        """
        Maneja la solicitud de autenticación.

        Args:
            kwargs: Argumentos adicionales de la solicitud.

        Returns:
            object: El controlador destino si la autenticación es exitosa, de lo contrario, una respuesta de error.
        """

        # Obtener la clave de API y el token de autorización de las cabeceras
        token = self.request.headers.get('Authorization')

        # Realizar la validación de la clave de API
        if (token):

            # Montar el controlador destino-
            return Mount.controller(
                next=self.next,
                flask_request=self.request,
                arguments=kwargs
            )

        else:

            # Informar que se carece de credenciales validas.
            return JsonResponse.unauthorized(
                message="La petición carece de una autenticación valida."
            )

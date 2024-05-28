import requests

class Request:

    """
    Esta clase permite realizar peticiones HTTP para consumo de Servicios APIRest y SOAP.
    Los retornos siempre serán un JSON sin importar el error de consumo del EndPoint.
    """

    @staticmethod
    def post(url,params=None,headers=None):
        """
        Ejecutar peticiones POST

        Args:
            url (str): Base URL para las peticiones.
            params (json, optional): Cuerpo de la petición JSON. Por defecto, None.
            headers (json, optional): Encabezados de la petición. Por defecto, None.

        Returns:
            dict: Respuesta de la petición HTTP.
        """
        try:
            return requests.post(url,json=params,headers=headers)
        except Exception as e:
            raise ValueError(f"[HTTP Request]: Error de conexón, '{e}'")

    @staticmethod
    def get(url,params=None,headers=None):
        """
        Ejecutar peticiones GET

        Args:
            url (str): Base URL para las peticiones.
            params (json, optional): Query de la petición JSON. Por defecto, None.
            headers (json, optional): Encabezados de la petición. Por defecto, None.

        Returns:
            dict: Respuesta de la petición HTTP.
        """
        try:
            return requests.get(url,params=params,headers=headers)
        except Exception as e:
            raise ValueError(f"[HTTP Request]: Error de conexón, '{e}'")

    @staticmethod
    def sesion(url,params=None):
        """
        Este método es específico para hacer peticiones de inicio de sesión.
        En cualquier sistema a través de servicio REST.
        Peticiones para iniciar sesión saltando Captcha.

        Args:
            url (str): URL de inicio de sesión.
            params (json, optional): Parámetros de la petición. Por defecto, None.

        Returns:
            dict: Respuesta de la petición HTTP.
        """
        try:
            session = requests.Session()
            session.post(url,data=params)
            return session
        except Exception as e:
            raise ValueError(f"[HTTP Request]: Imposible Autenticar: '{e}'")

    @staticmethod
    def soap():
        """
        Permite definir que se aplicarán peticiones SOAP.

        Returns:
            RequestSoap: Objeto para realizar peticiones SOAP.
        """
        return RequestSoap

class RequestSoap:
    """
    Esta clase permite realizar peticiones SOAP a WebServices.
    Aplica los conceptos de la API REST a servicios SOAP.
    """

    @staticmethod
    def post(url, data=None, headers=None):
        """
        Este método permite hacer peticiones POST para consumo de servicios SOAP.

        Args:
            url (str): URL del servicio SOAP.
            data (str, optional): Datos para la petición. Por defecto, None.
            headers (json, optional): Encabezados de la petición. Por defecto, None.

        Returns:
            Response: Respuesta de la petición HTTP.
        """
        try:
            response = requests.post(url, data=data.encode('utf-8'),headers=headers)
            return response
        except Exception as e:
            raise ValueError(f"[HTTP XML Request]: Error de conexón, '{e}'")
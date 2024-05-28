import hmac
import base64
from lib.environment.config import Config

class Hash:

    # Ejecuta Hash sobre el valor suministrado.
    @staticmethod
    def make(value):
        """
        Genera un hash HMAC para el valor proporcionado utilizando SHA-512.

        Args:
            value (str or bytes): El valor para el cual se generará el hash.

        Returns:
            str: El hash HMAC en base64 URL-safe.
        """
        # Convertir la clave privada a bytes (si es una cadena)
        value_bytes = value.encode() if isinstance(value, str) else value

        # Calcular el HMAC de la clave privada utilizando SHA-512
        h = hmac.new(value_bytes, value_bytes, 'sha512')

        # Obtener el resultado del HMAC como bytes
        hmac_result = h.digest()

        # Codificar el resultado del HMAC en base64
        return base64.urlsafe_b64encode(hmac_result).decode()

    # Retona el Hask de la llave de la App.
    @staticmethod
    def key():
        """
        Retorna el hash HMAC de la clave de la aplicación.

        Returns:
            str: El hash HMAC de la clave de la aplicación en base64 URL-safe.
        """
        # Obtener la clave privada desde el entorno
        value = Config.app("key")

        # Convertir la clave privada a bytes (si es una cadena)
        value_bytes = value.encode() if isinstance(value, str) else value

        # Calcular el HMAC de la clave privada utilizando SHA-512
        h = hmac.new(value_bytes, value_bytes, 'sha512')

        # Obtener el resultado del HMAC como bytes
        hmac_result = h.digest()

        # Codificar el resultado del HMAC en base64
        return base64.urlsafe_b64encode(hmac_result).decode()
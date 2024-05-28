from flask import jsonify, send_file, redirect

class JsonResponse():
    """
    Esta clase proporciona métodos estáticos para generar respuestas JSON comunes
    utilizadas en servicios web. Contiene métodos para devolver respuestas de éxito,
    errores de cliente, errores de servidor y otros códigos de respuesta comunes.

    Los métodos de esta clase devuelven una tupla que contiene un objeto JSON y un
    código de estado HTTP que se utilizará para responder a las solicitudes HTTP.
    """

    @staticmethod
    def badRequest(status="Bad Request", message="Processing Error"):
        """
        Devuelve una respuesta de error de cliente (400 Bad Request).

        Args:
            status (str): El estado del error. Por defecto es "Bad Request".
            message (str): El mensaje de error. Por defecto es "Processing Error".

        Returns:
            tuple: Una tupla que contiene un objeto JSON y el código de estado HTTP 400.
        """
        return jsonify({
            "code": 400,
            "status": status,
            "message": message,
        }), 400

    @staticmethod
    def success(status="Ok", message="Process Successful", data=None):
        """
        Devuelve una respuesta de éxito (200 OK).

        Args:
            status (str): El estado del éxito. Por defecto es "Ok".
            message (str): El mensaje de éxito. Por defecto es "Process Successful".
            data (list): Los datos asociados al éxito. Por defecto es una lista vacía.

        Returns:
            tuple: Una tupla que contiene un objeto JSON y el código de estado HTTP 200.
        """
        response = {
            "code": 200,
            "status": status,
            "message": message
        }

        if data is not None:
            response["data"] = data

        return jsonify(response), 200

    @staticmethod
    def unauthorized(status="Unauthorized", message="Invalid credentials"):
        """
        Devuelve una respuesta de error de autorización (401 Unauthorized).

        Args:
            status (str): El estado del error de autorización. Por defecto es "Unauthorized".
            message (str): El mensaje de error de autorización. Por defecto es "Invalid credentials".

        Returns:
            tuple: Una tupla que contiene un objeto JSON y el código de estado HTTP 401.
        """
        return jsonify({
            "code": 401,
            "status": status,
            "message": message
        }), 401

    @staticmethod
    def notFound(status="Not Found", message="No values found to return"):
        """
        Devuelve una respuesta de error de recurso no encontrado (404 Not Found).

        Args:
            status (str): El estado del error de recurso no encontrado. Por defecto es "Not Found".
            message (str): El mensaje de error de recurso no encontrado. Por defecto es "No values found to return".

        Returns:
            tuple: Una tupla que contiene un objeto JSON y el código de estado HTTP 404.
        """
        return jsonify({
            "code": 404,
            "status": status,
            "message": message
        }), 404

    @staticmethod
    def serverError(status="Internal Server Error", message="General Exception"):
        """
        Devuelve una respuesta de error de servidor (500 Internal Server Error).

        Args:
            status (str): El estado del error de servidor. Por defecto es "Internal Server Error".
            message (str): El mensaje de error de servidor. Por defecto es "General Exception".

        Returns:
            tuple: Una tupla que contiene un objeto JSON y el código de estado HTTP 500.
        """
        return jsonify({
            "code": 500,
            "status": status,
            "message": message
        }), 500

    @staticmethod
    def unprocessable(status="Unprocessable Entity", message="Requirements for processing not satisfied"):
        """
        Devuelve una respuesta de error de entidad no procesable (422 Unprocessable Entity).

        Args:
            status (str): El estado del error de entidad no procesable. Por defecto es "Unprocessable Entity".
            message (str): El mensaje de error de entidad no procesable. Por defecto es "Requirements for processing not satisfied".

        Returns:
            tuple: Una tupla que contiene un objeto JSON y el código de estado HTTP 422.
        """
        return jsonify({
            "code": 422,
            "status": status,
            "message": message
        }), 422

    @staticmethod
    def dynamic(code, status, message, data=[]):
        """
        Devuelve una respuesta personalizada con un código de estado dinámico.

        Args:
            code (int): El código de estado HTTP.
            status (str): El estado de la respuesta.
            message (str): El mensaje de la respuesta.
            data (list): Los datos asociados a la respuesta. Por defecto es una lista vacía.

        Returns:
            tuple: Una tupla que contiene un objeto JSON y el código de estado HTTP especificado.
        """
        return jsonify({
            "code": code,
            "status": status,
            "message": message,
            "data":data
        }), code

    @staticmethod
    def fromObject(code, object={}):
        """
        Devuelve una respuesta JSON desde un objeto Python con un código de estado especificado.

        Args:
            code (int): El código de estado HTTP.
            object (dict): El objeto Python que se convertirá a JSON. Por defecto es un diccionario vacío.

        Returns:
            tuple: Una tupla que contiene un objeto JSON y el código de estado HTTP especificado.
        """
        return jsonify(object), code

class FileResponse:
    """
    Esta clase proporciona métodos estáticos para el envío de archivos a través de
    respuestas HTTP. Contiene métodos para envío de archivos de texto y Excel.

    Los métodos de esta clase utilizan la función `send_file` de Flask para enviar
    archivos al cliente.
    """

    @staticmethod
    def txt(filename):
        """
        Devuelve una respuesta HTTP para la descarga de un archivo de texto.

        Args:
            filename (str): El nombre del archivo de texto.

        Returns:
            Flask.Response: Una respuesta HTTP para la descarga del archivo de texto.
        """
        return send_file(filename, as_attachment=True)

    @staticmethod
    def excel(filename):
        """
        Devuelve una respuesta HTTP para la descarga de un archivo Excel.

        Args:
            filename (str): El nombre del archivo Excel.

        Returns:
            Flask.Response: Una respuesta HTTP para la descarga del archivo Excel.
        """
        return send_file(filename, as_attachment=True)

class Redirect:

    @staticmethod
    def to(url:str):

        """
        Este metodo redirecciona a una URL externa del Sistema
        Se requiere que la URL se use completa o minimo de la siguiente forma 
        (//google.com.co) esto si se desconoce si es http// ó https://
        """
        return redirect(url)
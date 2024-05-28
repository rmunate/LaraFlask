import json
import os
import base64
from lib.clarity.paths import Paths

class Storage:

    """
    Esta clase permite manipular los archivos del sistema de una forma simple.
    Al igual que acceder a las rutas de los mismos.
    Contenido dentro del Storage.
    """

    @staticmethod
    def path(name:str=None):
        """
        Retorna la ruta completa de archivos incluyendo el nombre del archivo.

        Args:
            name (str): El nombre del archivo.

        Returns:
            str: La ruta completa del archivo.
        """
        basePath = Paths.storage()

        if not os.path.exists(basePath):
            os.makedirs(basePath)

        if name is not None:
            path = os.path.join(basePath, name)
        else:
            path = basePath

        return path

    @staticmethod
    def delete(name):
        """
        Elimina el archivo pasando simplemente el nombre con la extensión (archivo.txt).

        Args:
            name (str): El nombre del archivo a eliminar.

        Returns:
            bool: True si la eliminación del archivo fue exitosa.

        Raises:
            ValueError: Si la eliminación del archivo falla.
        """
        try:
            file = os.path.join(Paths.storage(), name)

            if os.path.exists(file):
                os.remove(file)

            return True

        except Exception as e:

            raise ValueError(f"[Storage]: Error al eliminar el archivo '{name}', {e}")

    @staticmethod
    def put_base64(name, content):
        """
        Permite guardar un archivo de acuerdo a su contenido equivalente en base64.

        Args:
            name (str): El nombre del archivo a guardar.
            content (str): El contenido del archivo en formato base64.

        Returns:
            bool: True si la guardado del archivo desde base64 fue exitoso.

        Raises:
            ValueError: Si ocurre un error al guardar el archivo desde base64.
        """
        try:
            bytes = base64.b64decode(content)
            file_path = os.path.join(Paths.storage(), name)

            with open(file_path, 'wb') as f:
                f.write(bytes)

            return True

        except Exception as e:

            raise ValueError(f"[Storage]: Error Al Guardar Desde Base64, {e}")

    @staticmethod
    def put_json(name, content):
        """
        Permite guardar un archivo de acuerdo a su contenido JSON.

        Args:
            name (str): El nombre del archivo a guardar.
            content (str): El contenido del archivo en formato base64.

        Returns:
            bool: True si la guardado del archivo desde base64 fue exitoso.

        Raises:
            ValueError: Si ocurre un error al guardar el archivo desde base64.
        """
        try:
            file_path = os.path.join(Paths.storage(), name)

            with open(file_path, 'w') as f:
                json.dump(content, f, indent=4)

            return True

        except Exception as e:

            raise ValueError(f"[Storage]: Error Al Guardar Archivo, {e}")

    @staticmethod
    def list(subdirectory:str = None, full_path = False):

        """
        Este metodo lista todo el contenido de archivos de la carpeta Files
        """
        if subdirectory is not None:
            list = os.listdir(Storage.path(subdirectory))
        else:
            list = os.listdir(Paths.storage())

        files = []

        for file in list:
            fullpath = Storage.path(name=file)
            if os.path.isfile(fullpath):
                if full_path:
                    files.append(fullpath)
                else:
                    files.append(file)

        return files

    @staticmethod
    def get_content(name:str):

        """
        Este metodo retorna el contenido de un archivo.
        """

        try:
            file = os.path.join(Paths.storage(), name)

            if os.path.exists(file):

                 with open(file, 'r') as archivo:
                    contenido = archivo.read()
                    return contenido

            return None

        except Exception as e:

            raise ValueError(f"[Storage]: Error al leer el archivo '{name}', {e}")

    @staticmethod
    def get_json(name:str):

        """
        Este metodo retorna el contenido de un archivo.
        """

        try:
            file = os.path.join(Paths.storage(), name)

            if os.path.exists(file):

                with open(file, 'r') as f:
                    return json.load(f)

            return None

        except Exception as e:

            raise ValueError(f"[Storage]: Error al leer el archivo '{name}', {e}")
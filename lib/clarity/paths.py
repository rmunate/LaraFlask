import os

class Paths:

    """
    Esta clase se encarga de retornar las rutas de acceso a las diferentes
    carpetas que se emplean dentro de la aplicación.
    """

    @staticmethod
    def app(file=None):
        """
        Retorna la ruta de la carpeta 'app' del proyecto.

        Args:
            file (str, optional): Nombre de un archivo dentro de la carpeta 'app'. Por defecto, None.

        Returns:
            str: La ruta de la carpeta 'app' o de un archivo dentro de ella.
        """
        session_path = os.path.join(Paths.base(), 'app')
        if file is not None:
            session_path = os.path.join(session_path, file)
        return session_path

    @staticmethod
    def config(file=None):
        """
        Retorna la ruta de la carpeta 'config' del proyecto.

        Args:
            file (str, optional): Nombre de un archivo dentro de la carpeta 'config'. Por defecto, None.

        Returns:
            str: La ruta de la carpeta 'config' o de un archivo dentro de ella.
        """
        session_path = os.path.join(Paths.base(), 'config')
        if file is not None:
            session_path = os.path.join(session_path, file)
        return session_path

    @staticmethod
    def public(file=None):
        """
        Retorna la ruta de la carpeta 'public' del proyecto.

        Args:
            file (str, optional): Nombre de un archivo dentro de la carpeta 'public'. Por defecto, None.

        Returns:
            str: La ruta de la carpeta 'public' o de un archivo dentro de ella.
        """
        session_path = os.path.join(Paths.base(), 'public')
        if file is not None:
            session_path = os.path.join(session_path, file)
        return session_path

    @staticmethod
    def routes(file=None):
        """
        Retorna la ruta de la carpeta 'routes' del proyecto.

        Args:
            file (str, optional): Nombre de un archivo dentro de la carpeta 'routes'. Por defecto, None.

        Returns:
            str: La ruta de la carpeta 'routes' o de un archivo dentro de ella.
        """
        session_path = os.path.join(Paths.base(), 'routes')
        if file is not None:
            session_path = os.path.join(session_path, file)
        return session_path

    @staticmethod
    def resources(file=None):
        """
        Retorna la ruta de la carpeta 'resources' del proyecto.

        Args:
            file (str, optional): Nombre de un archivo dentro de la carpeta 'resources'. Por defecto, None.

        Returns:
            str: La ruta de la carpeta 'resources' o de un archivo dentro de ella.
        """
        session_path = os.path.join(Paths.base(), 'resources')
        if file is not None:
            session_path = os.path.join(session_path, file)
        return session_path

    @staticmethod
    def views(file=None):
        """
        Retorna la ruta de la carpeta 'views' del proyecto.

        Args:
            file (str, optional): Nombre de un archivo dentro de la carpeta 'views'. Por defecto, None.

        Returns:
            str: La ruta de la carpeta 'views' o de un archivo dentro de ella.
        """
        views_path = os.path.join(Paths.base(), 'resources', 'views')
        if file is not None:
            views_path = os.path.join(views_path, file)
        return views_path

    @staticmethod
    def storage(file=None):
        """
        Retorna la ruta de la carpeta 'storage' del proyecto.

        Args:
            file (str, optional): Nombre de un archivo dentro de la carpeta 'storage'. Por defecto, None.

        Returns:
            str: La ruta de la carpeta 'storage' o de un archivo dentro de ella.
        """
        session_path = os.path.join(Paths.base(), 'storage')
        if file is not None:
            session_path = os.path.join(session_path, file)
        return session_path

    @staticmethod
    def tests(file=None):
        """
        Retorna la ruta de la carpeta 'tests' del proyecto.

        Args:
            file (str, optional): Nombre de un archivo dentro de la carpeta 'tests'. Por defecto, None.

        Returns:
            str: La ruta de la carpeta 'tests' o de un archivo dentro de ella.
        """
        session_path = os.path.join(Paths.base(), 'tests')
        if file is not None:
            session_path = os.path.join(session_path, file)
        return session_path

    @staticmethod
    def lib(file=None):
        """
        Retorna la ruta de la carpeta 'lib' del proyecto.

        Args:
            file (str, optional): Nombre de un archivo dentro de la carpeta 'lib'. Por defecto, None.

        Returns:
            str: La ruta de la carpeta 'lib' o de un archivo dentro de ella.
        """
        session_path = os.path.join(Paths.base(), 'lib')
        if file is not None:
            session_path = os.path.join(session_path, file)
        return session_path

    @staticmethod
    def base(file=None):
        """
        Retorna la ruta base del proyecto.

        Args:
            file (str, optional): Nombre de un archivo dentro de la ruta base. Por defecto, None.

        Returns:
            str: La ruta base o de un archivo dentro de ella.
        """
        base_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), '../../')
        if file is not None:
            base_path = os.path.join(base_path, file)
        return base_path

    @staticmethod
    def session(file=None):
        """
        Retorna la ruta al directorio de sesiones.

        Args:
            file (str, optional): Nombre de un archivo dentro del directorio de sesiones. Por defecto, None.

        Returns:
            str: La ruta al directorio de sesiones o de un archivo dentro de ella.
        """
        session_path = os.path.join(Paths.base(), 'storage', 'session')
        if file is not None:
            session_path = os.path.join(session_path, file)
        return session_path

    @staticmethod
    def log(file=None):
        """
        Retorna la ruta al directorio de logs.

        Args:
            file (str, optional): Nombre de un archivo dentro del directorio de logs. Por defecto, None.

        Returns:
            str: La ruta al directorio de logs o de un archivo dentro de ella.
        """
        session_path = os.path.join(Paths.base(), 'storage', 'log')
        if file is not None:
            session_path = os.path.join(session_path, file)
        return session_path

    @staticmethod
    def files(file=None):
        """
        Retorna la ruta al directorio de archivos (storage/files).

        Args:
            file (str, optional): Nombre de un archivo dentro del directorio de archivos. Por defecto, None.

        Returns:
            str: La ruta al directorio de archivos o de un archivo dentro de ella.
        """
        session_path = os.path.join(Paths.base(), 'storage', 'files')
        if file is not None:
            session_path = os.path.join(session_path, file)
        return session_path
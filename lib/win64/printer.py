import subprocess
import platform
import os

class WindowsPrinter:
    """
    Esta clase permite lanzar impresiones a niveles de Windows de archivos en extensión PDF.
    Esto aplica solo para impresoras multifuncionales. No aplica para impresoras térmicas u otras.
    """

    @staticmethod
    def fromPDF(file, printer, copies = 1):
        """
        Imprime un archivo PDF en una impresora especificada.

        Args:
            file (str): Ruta del archivo PDF que se imprimirá.
            printer (str): Nombre de la impresora a la que se enviará la impresión.
            copies (int, opcional): Cantidad de copias a imprimir. Por defecto es 1.

        Returns:
            bool: True si la impresión se realizó correctamente, False de lo contrario.

        Raises:
            ValueError: Si ocurre algún error durante el proceso de impresión.
        """

        # Intento de impresion
        try:

            operative_system = platform.system()

            # Verificar si el sistema operativo es Windows
            is_windows = (operative_system == 'Windows')

            # Verificar si el sistema operativo es Windows Server
            is_windows_server = operative_system and ('server' in platform.win32_ver()[0].lower())

            # Definir el Driver a usar para imprmir
            if is_windows and is_windows_server:
                driverName = 'PDFtoPrinterServer.exe'
            elif is_windows:
                driverName = 'PDFtoPrinterClient.exe'
            else:
                raise ValueError("[Print] No se reconoce la version de Windows en Uso.")

            # Copias
            copies = f"copies={copies}"

            # Especifica la ruta del archivo PDF y el nombre de la impresora
            exe_path = os.path.join(os.path.dirname(__file__), "drivers", driverName)

            # Ejecuta el comando PDFtoPrinter.exe desde Python
            output = subprocess.run([exe_path, file, printer, copies], capture_output=True, text=True, shell=True)

            # Determinar Si Hay Error
            if 'not found' in output.stdout or 'is not valid' in output.stdout:
                raise ValueError(output.stdout)

            # Retorno De Salida
            return True

        except Exception as e:

            # Retorno de Bandera
            raise ValueError(f"[Pinter]: Error de impresion, {e}")
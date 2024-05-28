import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email import encoders
from lib.clarity.file import File
from lib.environment.config import Config

class Email:
    """
    Esta clase proporciona métodos para enviar correos electrónicos mediante SMTP.
    Permite configurar el remitente, destinatarios, asunto, cuerpo del mensaje,
    adjuntos y enviar el correo electrónico.
    """

    def __init__(self, sender='default'):
        """
        Inicializa la clase Email con la configuración del remitente.

        Args:
            sender (str): El nombre del remitente configurado.
        """
        # Valores a Poblar
        self.subjectEmail = None
        self.toAddresses = None
        self.text = None
        self.html_string = None
        self.attachments = []

        # Define el sender:
        senderData = Config.mail(sender)

        if senderData is None:
            raise ValueError(f"[Mail]: No se encontró una configuracion de correo electronico para: '{sender}'")

        self.server = senderData["host"]
        self.port = senderData["port"]
        self.username = senderData["username"]
        self.password = senderData["password"]
        self.fromAddress = senderData["address"]

    def subject(self, subject):
        """
        Establece el asunto del correo electrónico.

        Args:
            subject (str): El asunto del correo.
        """
        self.subjectEmail = subject

    def to(self, to):
        """
        Establece los destinatarios del correo electrónico.

        Args:
            to (list): Lista de direcciones de correo electrónico de los destinatarios.
        """
        self.toAddresses = to

    def textPlain(self, text):
        """
        Establece el cuerpo del correo electrónico en formato de texto plano.

        Args:
            text (str): El cuerpo del correo en texto plano.
        """
        self.text = text

    def html(self, html:str):
        """
        Establece el cuerpo del correo electrónico utilizando un archivo HTML como plantilla.

        Args:
            html (str): La ruta al archivo HTML de la plantilla.
        """
        self.html_string = html

    def file(self, file):
        """
        Agrega un archivo como adjunto al correo electrónico.

        Args:
            file (str): La ruta al archivo que se adjuntará.
        """
        file = File.path(file)
        if os.path.exists(file):
            self.attachments.append(file)

    def send(self):
        """
        Envía el correo electrónico utilizando el servidor SMTP configurado.
        """
        try:

            # Valores Globales de origen
            email = MIMEMultipart()
            email["From"] = self.fromAddress
            email["To"] = ", ".join(self.toAddresses)
            email["Subject"] = self.subjectEmail

            if self.html_string is not None and self.html != '':
                email.attach(MIMEText(self.html_string, "html", "utf-8"))
            else:
                email.attach(MIMEText(self.text, "plain", "utf-8"))

            # Adjuntar Archivos. (De Existir)
            for archivo in self.attachments:
                nombre_adjunto = os.path.basename(archivo)

                parte_adjunta = MIMEBase("application", "octet-stream")
                parte_adjunta.set_payload(open(archivo, "rb").read())
                encoders.encode_base64(parte_adjunta)
                parte_adjunta.add_header("Content-Disposition", f"attachment; filename= {nombre_adjunto}")
                email.attach(parte_adjunta)

            # Envio de correo.
            with smtplib.SMTP(self.server, self.port) as server:
                server.starttls()
                server.login(self.username, self.password)
                server.send_message(email)

        except Exception as error:

            raise ValueError(f"[Email]: Error al enviar correo. {error}")
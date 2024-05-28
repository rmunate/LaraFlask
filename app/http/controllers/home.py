from lib.http.response import Redirect

class Homecontroller:

    def index(self):

        """Redirecciona a la pagina principal del CCL"""

        return Redirect.to("https://www.google.com.co/")
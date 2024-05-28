from jinja2 import Environment, FileSystemLoader, select_autoescape
from lib.clarity.paths import Paths

class View:
    """
    Esta clase permite ejecutar acciones con vistas HTML utilizando Jinja2.
    """

    @staticmethod
    def make(template:str, vars=None):
        """
        Crea una instancia de ViewActions para renderizar un template HTML.
        """
        env = Environment(
            loader=FileSystemLoader(Paths.views()),
            autoescape=select_autoescape(['html', 'xml'])
        )

        template_obj = env.get_template(f"{template}.html")
        return ViewActions(template_obj, vars)

class ViewActions:
    """
    Clase con todas las acciones posibles sobre los templates HTML del sistema.
    """

    def __init__(self, template_obj, vars=None):

        self.template_obj = template_obj
        self.vars = vars or {}

    def render(self):
        """
        Renderiza el template HTML con las variables especificadas.
        """
        return self.template_obj.render(**self.vars)

    def html(self):
        """
        Retorna el contenido HTML del template.
        """
        return self.template_obj.template_source
from datetime import datetime, timedelta, timezone

class Clock:
    """
    Esta clase permite definir el timezone a usar.
    Adicionalmente, permite retornar una hora que sea válida en dicho formato.
    """

    def __init__(self, zone=-5):
        """
        Inicializa la clase con el timezone especificado.

        Args:
            zone (int, optional): El desplazamiento horario respecto al UTC. Por defecto, es -5.
        """
        tz = timezone(timedelta(hours=zone))
        self.timezone = datetime.now(tz)

    def to(self, hour,minute,second):
        """
        Retorna una hora válida en la zona horaria determinada.

        Args:
            hour (int): La hora deseada.
            minute (int): El minuto deseado.
            second (int): El segundo deseado.

        Returns:
            str: Una cadena de texto que representa la hora válida en el formato "HH:MM".
        """
        start_time = self.timezone.replace(hour=hour, minute=minute, second=second, microsecond=0)
        return start_time.strftime("%H:%M")
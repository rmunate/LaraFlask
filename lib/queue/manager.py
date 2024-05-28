import queue
import threading

class QueueManager:

    """
    Clase para gestionar múltiples colas de manera centralizada utilizando el patrón Singleton.

    Esta clase permite crear, agregar tareas y procesar colas de forma segura en un entorno multi-hilo.

    Uso:
        # Obtener la instancia única del QueueManager
        queue_manager = QueueManager()

        # Crear una nueva cola
        queue_manager.create_queue('cola1')

        # Agregar tarea a una cola existente
        queue_manager.enqueue_task('cola1', 'tarea1')

        # Iniciar el procesamiento de una cola en un hilo separado
        queue_manager.start_processing('cola1')
    """

    _instance = None  # Instancia única del QueueManager

    def __new__(cls):
        """
        Crea una instancia única del QueueManager utilizando el patrón Singleton.

        Returns:
            QueueManager: Instancia única del QueueManager.
        """
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.queues = {}  # Diccionario para almacenar las colas
        return cls._instance

    def create_queue(self, name):
        """
        Crea una nueva cola con el nombre especificado.

        Args:
            name (str): Nombre de la cola a crear.

        Returns:
            None
        """
        self.queues[name] = queue.Queue()

    def enqueue_task(self, queue_name, task):
        """
        Agrega una tarea a la cola especificada.

        Args:
            queue_name (str): Nombre de la cola.
            task (object): Tarea a agregar a la cola.

        Raises:
            ValueError: Si la cola especificada no existe.

        Returns:
            None
        """
        if queue_name in self.queues:
            self.queues[queue_name].put(task)
        else:
            raise ValueError(f"La cola '{queue_name}' no existe.")

    def process_queue(self, queue_name):
        """
        Procesa la cola especificada de manera secuencial en un hilo separado.

        Args:
            queue_name (str): Nombre de la cola a procesar.

        Returns:
            None
        """
        def _process():
            while True:
                task = self.queues[queue_name].get()
                # Procesar la tarea aquí (por ejemplo, imprimir la tarea)
                print(f"Procesando tarea en '{queue_name}': {task}")
                self.queues[queue_name].task_done()

        threading.Thread(target=_process, daemon=True).start()

    def start_processing(self, queue_name):
        """
        Inicia el procesamiento de la cola especificada en un hilo separado.

        Args:
            queue_name (str): Nombre de la cola a procesar.

        Raises:
            ValueError: Si la cola especificada no existe.

        Returns:
            None
        """
        if queue_name in self.queues:
            self.process_queue(queue_name)
        else:
            raise ValueError(f"La cola '{queue_name}' no existe.")


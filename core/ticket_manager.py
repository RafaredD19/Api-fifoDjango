from .models import Ticket
from django.utils import timezone
import json
import os

class TicketManager:
    FILE_PATH = 'tickets.json'  # Ruta del archivo JSON para almacenar el estado

    def add_ticket(self, client_name, priority):
        """
        Complejidad: O(1)
        Agregar un ticket a la base de datos es una operación constante,
        ya que se inserta una nueva instancia de Ticket directamente en la base de datos.
        """
        ticket = Ticket(client_name=client_name, priority=priority, timestamp=timezone.now())
        ticket.save()
        self.save_to_file()  # Guardar estado en archivo JSON después de añadir
        return ticket

    def get_next_ticket(self):
        """
        Complejidad: O(1) para obtener el primer ticket; O(n) para la eliminación.
        Django obtiene el primer ticket con una consulta constante, pero eliminarlo implica
        reorganizar internamente la base de datos, lo cual es O(n) en el peor caso.
        """
        next_ticket = Ticket.objects.order_by('timestamp').first()  # FIFO: obtener el ticket más antiguo
        if next_ticket:
            next_ticket.delete()
            self.save_to_file()  # Guardar estado después de eliminar
        return next_ticket

    def get_all_tickets_sorted_by_priority(self):
        """
        Complejidad: O(n log n)
        Ordenar todos los tickets por prioridad implica una clasificación de lista,
        que Django implementa con un algoritmo de clasificación eficiente.
        """
        return Ticket.objects.order_by('priority')

    def get_all_tickets_sorted_by_timestamp(self):
        """
        Complejidad: O(n log n)
        Similar al ordenamiento por prioridad, la clasificación por timestamp también
        es O(n log n) dado que Django aplica un algoritmo de clasificación óptimo.
        """
        return Ticket.objects.order_by('timestamp')

    def search_ticket_by_id(self, ticket_id):
        """
        Complejidad: O(1) en promedio
        Buscar un ticket por ID es eficiente porque Django utiliza el índice de clave primaria,
        por lo que generalmente es una operación constante.
        """
        try:
            return Ticket.objects.get(id=ticket_id)
        except Ticket.DoesNotExist:
            return None

    def search_tickets_by_client_name(self, client_name):
        """
        Complejidad: O(n)
        La búsqueda por nombre del cliente recorre todos los registros, resultando en una
        complejidad lineal en el peor caso.
        """
        return Ticket.objects.filter(client_name__icontains=client_name)

    def save_to_file(self):
        """
        Complejidad: O(n)
        Convertir todos los tickets en una lista y escribir en un archivo es O(n),
        ya que involucra recorrer todos los tickets.
        """
        tickets = Ticket.objects.all().values('id', 'client_name', 'priority', 'timestamp')
        with open(self.FILE_PATH, 'w') as file:
            json.dump(list(tickets), file, default=str)

    def load_from_file(self):
        """
        Complejidad: O(n)
        Leer un archivo y cargar cada ticket en la base de datos es O(n),
        pues el proceso depende de la cantidad de tickets almacenados en el archivo.
        """
        if os.path.exists(self.FILE_PATH):
            with open(self.FILE_PATH, 'r') as file:
                data = json.load(file)
                for item in data:
                    Ticket.objects.get_or_create(
                        id=item['id'],
                        defaults={
                            'client_name': item['client_name'],
                            'priority': item['priority'],
                            'timestamp': item['timestamp']
                        }
                    )

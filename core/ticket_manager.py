from .models import Ticket
from django.utils import timezone
import json
import os

class TicketManager:
    FILE_PATH = 'tickets.json'  # Ruta del archivo JSON para almacenar el estado

    def add_ticket(self, client_name, priority):
        ticket = Ticket(client_name=client_name, priority=priority, timestamp=timezone.now())
        ticket.save()
        self.save_to_file()  # Guardar estado en archivo JSON después de añadir
        return ticket

    def get_next_ticket(self):
        # Obtener el siguiente ticket en orden FIFO y eliminarlo
        next_ticket = Ticket.objects.first()
        if next_ticket:
            next_ticket.delete()
            self.save_to_file()  # Guardar estado después de eliminar
        return next_ticket

    def get_all_tickets_sorted_by_priority(self):
        # Obtener todos los tickets ordenados por prioridad ascendente
        return Ticket.objects.order_by('priority')

    def save_to_file(self):
        # Guardar todos los tickets en un archivo JSON
        tickets = Ticket.objects.all().values('id', 'client_name', 'priority', 'timestamp')
        with open(self.FILE_PATH, 'w') as file:
            json.dump(list(tickets), file, default=str)  # `default=str` convierte fechas a string

    def load_from_file(self):
        # Cargar tickets desde el archivo JSON, si existe
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

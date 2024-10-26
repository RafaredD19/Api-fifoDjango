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
        # Obtener el ticket con el timestamp más antiguo (FIFO)
        next_ticket = Ticket.objects.order_by('timestamp').first()  # Ordenar por timestamp para FIFO
        if next_ticket:
            next_ticket.delete()
            self.save_to_file()  # Guardar estado después de eliminar
        return next_ticket

    def get_all_tickets_sorted_by_priority(self):
        # Obtener todos los tickets ordenados por prioridad en orden ascendente
        return Ticket.objects.order_by('priority')

    def get_all_tickets_sorted_by_timestamp(self):
        # Obtener todos los tickets ordenados por fecha/hora en orden ascendente
        return Ticket.objects.order_by('timestamp')

    def search_ticket_by_id(self, ticket_id):
        # Buscar un ticket por su ID
        try:
            return Ticket.objects.get(id=ticket_id)
        except Ticket.DoesNotExist:
            return None

    def search_tickets_by_client_name(self, client_name):
        # Buscar tickets por el nombre del cliente
        return Ticket.objects.filter(client_name__icontains=client_name)

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

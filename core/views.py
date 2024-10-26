from django.shortcuts import render
from .ticket_manager import TicketManager

ticket_manager = TicketManager()
ticket_manager.load_from_file()  # Cargar el estado desde el archivo al iniciar

def add_ticket_view(request):
    if request.method == 'POST':
        client_name = request.POST['client_name']
        priority = int(request.POST['priority'])
        ticket_manager.add_ticket(client_name, priority)
    return render(request, 'add_ticket.html')

def view_tickets(request):
    tickets = ticket_manager.get_all_tickets_sorted_by_priority()
    return render(request, 'view_tickets.html', {'tickets': tickets})

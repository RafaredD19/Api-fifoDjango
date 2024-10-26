from django.shortcuts import render, redirect
from django.http import HttpResponse
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
    # Obtener la lista de tickets ordenados por prioridad por defecto
    order_by = request.GET.get('order_by', 'priority')
    if order_by == 'timestamp':
        tickets = ticket_manager.get_all_tickets_sorted_by_timestamp()
    else:
        tickets = ticket_manager.get_all_tickets_sorted_by_priority()
    
    message = request.GET.get('message')
    return render(request, 'view_tickets.html', {'tickets': tickets, 'message': message})

def process_next_ticket_view(request):
    next_ticket = ticket_manager.get_next_ticket()
    if next_ticket:
        message = f"Procesado Ticket {next_ticket.id} - Cliente: {next_ticket.client_name}"
    else:
        message = "No hay tickets en la cola para procesar."
    return redirect(f"/tickets/view/?message={message}")

def search_ticket_view(request):
    # Buscar un ticket por ID o por nombre del cliente
    query = request.GET.get('query')
    search_by = request.GET.get('search_by', 'id')

    if search_by == 'client_name':
        tickets = ticket_manager.search_tickets_by_client_name(query)
    else:
        tickets = [ticket_manager.search_ticket_by_id(query)]

    return render(request, 'view_tickets.html', {'tickets': tickets, 'message': f"Resultados de búsqueda para '{query}'"})

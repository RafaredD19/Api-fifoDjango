from django.shortcuts import render, redirect
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
    # Mostrar la lista de tickets y un mensaje opcional si fue procesado
    tickets = ticket_manager.get_all_tickets_sorted_by_priority()
    message = request.GET.get('message')  # Obtener el mensaje desde la URL si existe
    return render(request, 'view_tickets.html', {'tickets': tickets, 'message': message})

def process_next_ticket_view(request):
    # Procesar el siguiente ticket en FIFO y redirigir a la lista de tickets con un mensaje
    next_ticket = ticket_manager.get_next_ticket()
    if next_ticket:
        message = f"Procesado Ticket {next_ticket.id} - Cliente: {next_ticket.client_name}"
    else:
        message = "No hay tickets en la cola para procesar."
    # Redirigir a la vista de tickets con el mensaje en la URL
    return redirect(f"/tickets/view/?message={message}")

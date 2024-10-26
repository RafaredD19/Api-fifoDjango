from django.urls import path
from . import views

urlpatterns = [
    path('add/', views.add_ticket_view, name='add_ticket'),
    path('view/', views.view_tickets, name='view_tickets'),
    path('process/', views.process_next_ticket_view, name='process_next_ticket'),
    path('search/', views.search_ticket_view, name='search_ticket'),
]

from django.urls import path
from . import views

urlpatterns = [
    path('add/', views.add_ticket_view, name='add_ticket'),
    path('view/', views.view_tickets, name='view_tickets'),
]

from django.db import models

class Ticket(models.Model):
    client_name = models.CharField(max_length=100)
    priority = models.IntegerField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Ticket {self.id} - {self.client_name}"

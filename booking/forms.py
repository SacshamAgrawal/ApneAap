from django import forms
from .models import Ticket

class TicketForm(forms.ModelForm):
    
    class Meta:
        model = Ticket
        fields = ("boarding_station_code","destination_station_code","no_of_tickets")

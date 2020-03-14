from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth import get_user_model


#User model 
user = get_user_model()

# Create your models here.
# class RailwayStation(models.Model):
#     """Model definition for RailwayStation."""

#     code = models.CharField(_("Station Code"), max_length=4,unique=True)
#     station_name = models.CharField(_("Station Name"), max_length=32,unique=True)

#     class Meta:
#         """Meta definition for RailwayStation."""

#         verbose_name = 'RailwayStation'
#         verbose_name_plural = 'RailwayStations'

#     def __str__(self):
#         """Unicode representation of RailwayStation."""
#         pass

class Ticket(models.Model):

    user = models.ForeignKey(user , on_delete = models.CASCADE)
    boarding_station_code = models.CharField(max_length=4 )
    destination_station_code = models.CharField( max_length=4)
    no_of_tickets = models.IntegerField(_("No. of Tickets"),default=1)
    ticket_id = models.AutoField(primary_key = True)

    class Meta:
        verbose_name = _("Ticket")
        verbose_name_plural = _("Tickets")

    def __str__(self):
        return str(self.ticket_id)
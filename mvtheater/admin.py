from django.contrib import admin

# Register your models here.
from mvtheater.models import Clients, Movies, Cinemas, Matinees, Tickets

admin.site.register(Clients)
admin.site.register(Movies)
admin.site.register(Cinemas)
admin.site.register(Matinees)


class TicketAdmin(admin.ModelAdmin):
    fields = ['matinee', 'client', 'transaction', 'state']
    search_fields = ['client__user__first_name', 'client__user__last_name']
    list_filter = ['client']
admin.site.register(Tickets, TicketAdmin)
from dataclasses import fields
from django.contrib import admin
from .models import Venue,MyClubUser,Event


# admin.site.register(Venue)
admin.site.register(MyClubUser)
# admin.site.register(Event)

# changing admin panel for venue model
@admin.register(Venue)
class VenueAdmin(admin.ModelAdmin):
    list_display = ('name' ,'address','phone')
    ordering = ('name',)
    search_fields = ('name','address')
    
@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    fields = (('name','venue'),'manager','event_date','description')
    list_display = ('name', 'event_date','venue')
    
    list_filter = ('event_date' , 'venue')
    ordering = ('event_date',)
    search_fields = ('name',)
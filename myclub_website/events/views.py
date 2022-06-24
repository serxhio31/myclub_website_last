import re
from urllib import response
from django.shortcuts import render, redirect
import calendar
from calendar import HTMLCalendar
from datetime import datetime
from django.http import HttpResponseRedirect, HttpResponse
from .models import Event, Venue
from django.contrib.auth.models import User
from .forms import VenueForm, EventForm, EventFormAdmin
from django.contrib.auth.models import User,auth
from django.contrib import messages
import csv

#Create my events page

def my_events(request):
    if request.user.is_authenticated:
        me = request.user.id
        events = Event.objects.filter(attendees=me)
        return render(request, 'events/my_events.html', {'events': events, 'me':me})
    else:
        messages.success(request, ("You are not authorized to view this Page!"))
        return redirect('home')


def venue_csv(request):
    response = HttpResponse(content_type = 'text/csv' )
    response['Content Disposition']= 'attachment; filename = venues.csv'
    
    #Create a csv writer
    writer = csv.writer(response)
    
    #Designate the model
    venues = Venue.objects.all()
    
    #Add column headings to the csv file
    writer.writerow(['Venue Name', 'Address','Zip Code', 'Phone','Web Address','Email'])
    
    #Loop Through and Output
    
    for venue in venues:
        writer.writerow([venue.name , venue.address, venue.zip_code , venue.phone , venue.web , venue.email_address])
    
    return response


def delete_venue(request, venue_id):
    venue = Venue.objects.get(id=venue_id)
    venue.delete()
    return redirect('list-venues')

def delete_event(request, event_id):
    event = Event.objects.get(id=event_id)
    if request.user == event.manager:
        event.delete()
        messages.success(request,("Event Deleted!"))
        return redirect('list-events')
    else:
        messages.success(request, ("You are not authorized to delete this Event!"))
        return redirect('list-events')


def update_event(request,event_id):
    event = Event.objects.get(id=event_id)
    if request.user.is_superuser:
        form = EventFormAdmin(request.POST or None, instance=event)
    else:
        form=EventForm(request.POST or None, instance=event)

    if form.is_valid():
        form.save()
        return redirect('list-events')
    return render(request, 'events/update_event.html', {'event' : event, 'form' : form})

def add_event(request):
    submitted = False
    if request.method == "POST":
        if request.user.is_superuser:
            form = EventFormAdmin(request.POST)
            if form.is_valid():
                form.save()
                return HttpResponseRedirect("/add_event?submitted=True")
        else:
            form = EventForm(request.POST)

            if form.is_valid():
                # form.save()
                event = form.save(commit=False)  # Save id's of users in venues.
                event.manager = request.user
                event.save()
                return HttpResponseRedirect("/add_event?submitted=True")
    else:
        #Just going to the page, not submitting
        if request.user.is_superuser:
            form = EventFormAdmin
        else:
            form = EventForm
        if 'submitted' in request.GET:
            submitted = True
    return render(request, 'events/add_event.html',{'form': form, 'submitted' : submitted})

def update_venue(request,venue_id):
    venue = Venue.objects.get(id=venue_id)
    form=VenueForm(request.POST or None, instance=venue)
    if form.is_valid():
        form.save()
        return redirect('list-venues')
    return render(request, 'events/update_venue.html', {'venue' : venue, 'form' : form})

# def register(request):
#     if request.method == 'POST':
#         username = request.POST['username']
#         email = request.POST['email']
#         password = request.POST['password']
#         password2 = request.POST['password2']
# #kontrollojme nese emaili eshte i njejte me repeated one dhe nese emaili ekziston me pare ne databaze
#         if password == password2:
#             if User.objects.filter(email=email).exists():
#                 messages.info(request, 'Email already used!')
#                 return redirect('register')
#             elif User.objects.filter(username=username).exists():
#                 messages.info(request, 'Username already used!')
#                 return redirect('register')
#             else:
#                 user = User.objects.create_user(username=username,email=email,password=password)
#                 user.save()
#                 return redirect('login')
#         else:
#             messages.info(request, 'Password is not the same!')
#             return redirect('register')
#     else:
#         return render(request, 'register.html')
#
# def login(request):
#     if request.method=='POST':
#         username =request.POST['username']
#         password = request.POST['password']
#
#         user = auth.authenticate(username=username ,password=password)
# #kontrollojme nese useri ekziston ne databaze apo jo
#         if user is not None:
#             auth.login(request,user)
#             return redirect('home')
#         else:
#             messages.info(request,'Credentials Invalid')
#             return redirect('login')
#
#     else:
#         return render(request ,'login.html')
#
# def logout(request):
#     auth.logout(request)
#     return redirect('home')

def search_venues(request):
    if request.method == "POST":
        searched = request.POST['searched']
        venues =Venue.objects.filter(name__contains=searched)
        return render(request, 'events/search_venues.html',{'searched' : searched,'venues': venues})
    else:
        return render(request, 'events/search_venues.html',{})
    
    

def show_venue(request,venue_id):
    venue = Venue.objects.get(id=venue_id)
    venue_owner = User.objects.get(id=venue.owner)
    return render(request, 'events/show_venue.html', {'venue' : venue, 'venue_owner':venue_owner})


def list_venues(request):
    venue_list = Venue.objects.all().order_by('name')
    return render(request, 'events/venues.html', {'venue_list' : venue_list})
    

    
def add_venue(request):
    submitted = False
    
    if request.method == "POST":
        form = VenueForm(request.POST)
        if form.is_valid():
            venue= form.save(commit=False) # Save id's of users in venues.
            venue.owner = request.user.id
            venue.save()
            form.save()
            return HttpResponseRedirect("/add_venue?submitted=True")
        
    else:
        form = VenueForm    
        if 'submitted' in request.GET:
            submitted = True
    return render(request, 'events/add_venue.html',{'form': form, 'submitted' : submitted})

def all_events(request):
    event_list = Event.objects.all().order_by('event_date')
    return render(request, 'events/event_list.html',
                  {'event_list' : event_list}
                  )

def home(request, year=datetime.now().year , month=datetime.now().strftime('%B')):
    dict = {"name" : "Sergio" , "lname" : "Merdani"}
    name = dict["name"]
    lname = dict["lname"]

    month = month.capitalize()

    #convert month from name to number

    month_number =list(calendar.month_name).index(month)
    month_number = int(month_number)

    #create calendar

    cal = HTMLCalendar().formatmonth(year,month_number)

    #get current year
    now = datetime.now()
    current_year = now.year

    #Get current time

    time = now.strftime('%I:%M %p')
    return render(request,
        'events/home.html',{
        "name" : name,
        "lname" : lname,
        "year" : year,
        "month" : month,
        "month_number" : month_number,
        "cal" : cal,
        "current_year" : current_year,
        "time" : time
    })
    
    

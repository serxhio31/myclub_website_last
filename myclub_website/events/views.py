from django.shortcuts import render
import calendar
from calendar import HTMLCalendar
from datetime import datetime

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
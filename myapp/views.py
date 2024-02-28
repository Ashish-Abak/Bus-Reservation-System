from django.shortcuts import render, redirect,HttpResponse
from myapp.models import User, Bus, Book
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from decimal import Decimal

# Create your views here.

def home(request):
    if request.user.is_authenticated:
        return render(request,'home.html')
    else:
        return render(request,'signin.html')


@login_required(login_url='signin')
def findbus(request):
    context = {}
    if request.method == 'POST':
        src = request.POST.get('source')
        desti = request.POST.get('destination')
        date = request.POST.get('date')
        bus_list = Bus.objects.filter(source=src, dest=desti, date=date)
        if bus_list:
            context['bus_list']=bus_list
            return render(request, 'list.html',context)
        else:
            context["error"] = "Sorry no buses availiable"
            return render(request, 'findbus.html', context)
    else:
        return render(request, 'findbus.html')


@login_required(login_url='signin')
def bookings(request):
    context = {}
    if request.method == 'POST':
        bid = request.POST.get('bus_id')
        seats = int(request.POST.get('no_seats'))
        bus = Bus.objects.get(id=bid)
        if bus.rem > int(seats):
            name_r = bus.bus_name
            cost = int(seats) * bus.price
            source_r = bus.source
            dest_r = bus.dest
            nos_r = Decimal(bus.nos)
            price_r = bus.price
            date_r = bus.date
            time_r = bus.time
            username_r = request.user.username
            email_r = request.user.email
            userid_r = request.user.id
            rem_r = bus.rem - seats
            Bus.objects.filter(id=bid).update(rem=rem_r)
            books = Book.objects.create(name=username_r, email=email_r, userid=userid_r, bus_name=name_r,source=source_r, 
                                        busid=bid,dest=dest_r, price=price_r, nos=seats, date=date_r, time=time_r,status='BOOKED')
            return render(request, 'bookings.html')
        else:
            context["error"] = "Sorry select fewer number of seats"
            return render(request, 'findbus.html', context)

    else:
        return render(request, 'findbus.html')


@login_required(login_url='signin')
def cancellings(request):
    context = {}
    if request.method == 'POST':
        id_r = request.POST.get('bus_id')
        book = Book.objects.filter(id=id_r).first()  
        if book is not None: 
            bus = Bus.objects.get(id=book.busid)
            rem_r = bus.rem + book.nos
            Bus.objects.filter(id=book.busid).update(rem=rem_r)
            Book.objects.filter(id=id_r).update(status='CANCELLED', nos=0)
            return redirect(seebookings)
        else:
            context["error"] = "Sorry, you have not booked that bus"
            return render(request, 'error.html', context)
    else:
        return render(request, 'findbus.html')



@login_required(login_url='signin')
def seebookings(request):
    context = {}
    id= request.user.id
    book_list = Book.objects.filter(userid=id)
    if book_list:
        context["book_list"] = book_list
        return render(request, 'booklist.html',context)
    else:
        context["error"] = "Sorry no buses booked"
        return render(request, 'findbus.html', context)


def signup(request):
    context = {}
    if request.method == 'POST':
        name_r = request.POST.get('name')
        email_r = request.POST.get('email')
        password_r = request.POST.get('password')
        user = User.objects.create_user(name_r, email_r, password_r )
        if user:
            login(request,user)
            return render(request, 'home.html')
        else:
            context["error"] = "Provide valid credentials"
            return render(request, 'signup.html', context)
    else:
        return render(request, 'signup.html', context)


def signin(request):
    context = {}
    if request.method == 'POST':
        name_r = request.POST.get('name')
        password_r = request.POST.get('password')
        user = authenticate(request, username=name_r, password=password_r)
        if user:
            login(request, user)
            return render(request, 'home.html')
        else:
            context["error"] = "Provide valid credentials"
            return render(request, 'signin.html', context)
    else:
        context["error"] = "You are not logged in"
        return render(request, 'signin.html', context)


def signout(request):
    logout(request)
    context={'error':"You have been logged out"}
    return render(request, 'signin.html', context)

def about(request):
    return render(request,'about.html')

def TC(request):
    return render(request,'T&C.html')

def pp(request):
    return render(request,'pp.html')

def contact(request):
    return render(request,'contact.html')
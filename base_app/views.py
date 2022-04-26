from django.shortcuts import render, redirect # for templates or pages
from django.http import HttpResponse
from django.contrib import messages # for flash messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q # for seqrch query
from django.contrib.auth.models import User # built-in user
from django.contrib.auth import authenticate, login, logout # built-in methods
from django.contrib.auth.forms import UserCreationForm # built-in usercreation form
from .models import Room, Topic # models
from .forms import RoomForm # custom forms


# Create your views here
# rooms = [
# {'id' : 1, 'name' : "Let's learn python"},
# {'id' : 2, 'name' : "Design with me"},
# {'id' : 3, 'name' : "Frontend developers"},
# ]

def loginUser(request):
    page = 'login'
    if request.user.is_authenticated:
        return redirect ('home')

    if request.method == 'POST':
        # Retrieve user credentials
        username = request.POST.get('username').lower()
        password = request.POST.get('password')

        #Check if that user exists
        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'User does not exist')

        # Makes sure the credentials of the existing user are correct
        # and get the user object that matches/based on the credentials.
        user = authenticate(request, username=username, password=password)

        # log in the user. This creates a session in the DB and the Browser
        if user is not None :
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Username OR password does not exist')

    context = {'page' : page}
    return render(request, 'registration/login_register.html', context)

def logoutUser(request):
    logout(request) # This is gonna delete the session token, therefore the user.
    return redirect('home')

def registerUser(request):
    form = UserCreationForm()

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False) # commit = to get the user obj right away to clean the data
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'An error occured during registration')

    return render(request, 'registration/login_register.html', {'form':form})

def home(request):
    # Search for the room based on the query/search params in the url
    #(i.e.by the topic name or room name )
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    rooms = Room.objects.filter(
        # icontains means that matches given characters from the full name
        Q(topic__name__icontains=q) |
        Q(name__icontains=q) |
        Q(description__icontains=q)

    )
    topics = Topic.objects.all() # get all the topics
    room_count = rooms.count() # get rooms count
    context =  {'rooms' : rooms, 'topics': topics, 'room_count': room_count}
    return render(request, 'base_app/home.html', context)

def room(request, pk):
    room = Room.objects.get(id=pk) # get a single object/room that matchs the attrib
    # for i in rooms:
    #     if i['id'] == int(pk):
    #         room = i
    context = {'room' : room }
    return render(request, 'base_app/room.html', context)

# only authenticated user can create room. Otherwise, redirect/force them to login
@login_required(login_url='login')
def createRoom(request):
    form = RoomForm()

    # Process data
    if request.method == 'POST':
        form = RoomForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')

    context = {'form': form}
    return render(request, 'base_app/room_form.html', context)

@login_required(login_url='login')
def updateRoom(request, pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)

    # If i know someone's room id i can just log in and
    # i'll be allowed to go ahead and update the room.
    # However, user who is not the owner of the room should not be allowed to update it
    if request.user != room.host :
        return HttpResponse('Your are not allowed here!!')

    if request.method == 'POST':
        form = RoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            return redirect('home')

    context = {'form' : form}
    return render(request, 'base_app/room_form.html', context)

@login_required(login_url='login')
def deleteRoom(request, pk):
    room = Room.objects.get(id=pk)

    # User who is not the owner of the room is not allowed to delete it
    if request.user != room.host :
        return HttpResponse('Your are not allowed here!!')

    if request.method == 'POST':
        room.delete()
        return redirect('home')

    context = {'obj' : room}
    return render(request, 'base_app/room_confirm_delete.html', context)

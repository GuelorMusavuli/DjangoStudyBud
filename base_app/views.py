from django.shortcuts import render, redirect # for templates or pages
from django.http import HttpResponse
from django.contrib import messages # for flash messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q # for seqrch query
from django.contrib.auth.models import User # built-in user
from django.contrib.auth import authenticate, login, logout # built-in methods
from django.contrib.auth.forms import UserCreationForm # built-in usercreation form
from .models import Room, Topic, Message # models
from .forms import RoomForm, UserForm # custom forms


# Create your views here
# rooms = [
# {'id' : 1, 'name' : "Let's learn python"},
# {'id' : 2, 'name' : "Design with me"},
# {'id' : 3, 'name' : "Frontend developers"},
# ]

def loginUser(request):
    page = 'login'

    # redirect user back to home page once authenticated to avoid displaying the login form again.
    if request.user.is_authenticated:
        return redirect ('home')

    # Processing of the user credentials to be logged in
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

        # log in the user and redirect them to the home page. This creates a session in the DB and the Browser
        if user is not None :
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Username OR password does not exist')

    context = {'page' : page}
    return render(request, 'registration/login-register.html', context)

def logoutUser(request):
    logout(request) # This is gonna delete the session token, therefore the user.
    return redirect('home')

def registerUser(request):
    form = UserCreationForm()

    # Processing of the user credentials to be created/registered
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

    return render(request, 'registration/login-register.html', {'form':form})

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

    # Filter recent activities(conversations) to a topic name or all.
    room_messages = Message.objects.filter(Q(room__topic__name__icontains=q))

    context =  {'rooms' : rooms, 'topics': topics, 'room_count': room_count, 'room_messages': room_messages}
    return render(request, 'base_app/home.html', context)

def room(request, pk):
    room = Room.objects.get(id=pk) # get a single object/room that matchs the attrib

    # query to the children objects of a specific room
    # in this case, get the set of all messages related to a specific room
    room_messages = room.message_set.all()

    # Get participants
    participants = room.participants.all()

    # Processing of the new participant's comments or messages to be added
    if request.method == 'POST':
        message = Message.objects.create(
            user = request.user, # logged i user
            room = room,
            body = request.POST.get('body') # body passed in the room_message form
        )
        # Add a new user to the ManyToManyField and render their info out in the participant section
        room.participants.add(request.user)

        # redirect the user to the room after entering the message
        return redirect ('room', pk=room.id)

    context = {'room' : room, 'room_messages': room_messages, 'participants': participants }
    return render(request, 'base_app/room.html', context)

def userProfile(request, pk):
    user = User.objects.get(id=pk)
    rooms = user.room_set.all()
    room_messages = user.message_set.all()
    topics = Topic.objects.all()
    context = {'user': user, 'rooms': rooms, 'room_messages': room_messages,'topics': topics}
    return render(request, 'registration/profile.html', context)



# only authenticated user can create room. Otherwise, redirect/force them to login
@login_required(login_url='login')
def createRoom(request):
    form = RoomForm()
    topics = Topic.objects.all()
    # Processing of the room data to be created
    if request.method == 'POST':
        topic_name = request.POST.get('topic') #from the form
        topic, created = Topic.objects.get_or_create(name=topic_name)

        Room.objects.create(
            host = request.user,
            topic = topic,
            name = request.POST.get('name'), #idem
            description = request.POST.get('description') #idem
        )
        # form = RoomForm(request.POST)
        # # if form.is_valid():
        # #     room = form.save(commit=False)
        # #     room.host = request.user # add the host based on who is logged in
        # #     room.save()
        return redirect('home')

    context = {'form': form, 'topics': topics}
    return render(request, 'base_app/create-update-room.html', context)

@login_required(login_url='login')
def updateRoom(request, pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)
    topics = Topic.objects.all()

    # If i know someone's room id i can just log in and
    # i'll be allowed to go ahead and update the room.
    # However, user who is not the owner of the room should not be allowed to update it
    if request.user != room.host :
        return HttpResponse('Your are not allowed here!!')

    # Processing of the room data to updated
    if request.method == 'POST':
        topic_name = request.POST.get('topic') #from the form
        topic, created = Topic.objects.get_or_create(name=topic_name)
        room.name = request.POST.get('name')
        room.topic = topic #newly created topic
        room.description = request.POST.get('description')
        room.save()

        # form = RoomForm(request.POST, instance=room)
        # if form.is_valid():
        #     form.save()

        return redirect('home')

    context = {'form' : form, 'topics': topics, 'room': room}
    return render(request, 'base_app/create-update-room.html', context)

@login_required(login_url='login')
def deleteRoom(request, pk):
    room = Room.objects.get(id=pk)

    # User who is not the owner of the room is not allowed to delete it
    if request.user != room.host :
        return HttpResponse('Your are not allowed here!!')

    # Processing of the room data to be deleted
    if request.method == 'POST':
        room.delete()
        return redirect('home')

    context = {'obj' : room}
    return render(request, 'base_app/delete.html', context)


@login_required(login_url='login')
def deleteMessage(request, pk):
    message = Message.objects.get(id=pk)

    # User who is not the owner of the message is not allowed to delete it
    if request.user != message.user :
        return HttpResponse('Your are not allowed here!!')

    # Processing of the message data to be deleted
    if request.method == 'POST':
        message.delete()
        return redirect('home')

    context = {'obj' : message}
    return render(request, 'base_app/delete.html', context)

@login_required(login_url='login')
def updateUser(request):
    user = request.user
    form = UserForm(instance=request.user)

    if request.method == 'POST':
        form = UserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('user-profile', pk=user.id)

    return render(request, 'registration/update-user.html', {'form': form})

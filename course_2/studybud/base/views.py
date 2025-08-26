from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.db.models import Q
from django.contrib import  messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from .models import Room, Topic, Message
from .forms import RoomForm, UserForm
from django.contrib.auth.decorators import login_required

# Auth View
def loginPage(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        username = request.POST.get('username').lower()
        password = request.POST.get('password')
        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, "User does not exist")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "Username or Password does not exist")
    return render(request, "base/login.html")

def logoutPage(request):
    logout(request)
    return redirect('home')
    return render(request, "base/home.html")

def registerPage(request):
    form = UserCreationForm()
    if request.method == "POST":
        form =  UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            try:
                login(request, user)
            except:
                messages.error(request, "User login failed.")
            return redirect('home')
        else:
            messages.error(request, "User register failed.")
    context = {'form':form}
    return render(request, "base/register.html", context)

# Public View
def home(request):    
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    rooms = Room.objects.filter(
        Q(topic__name__icontains=q) |
        Q(name__icontains=q) |
        Q(description__icontains=q)
    )
    topics = Topic.objects.all()
    room_count = len(rooms) | rooms.count()
    room_message = Message.objects.filter(
        Q(room__topic__name__icontains=q) 
    )
    context = {'rooms':rooms, "topics":topics, "room_count":room_count, 'room_message':room_message}
    return render(request, 'base/home.html',context)

def room(request, pk):
    room = Room.objects.get(id=pk)
    msgs = room.message_set.all().order_by('-created')
    body = request.POST.get('body')
    participants = room.participants.all()
    if request.method == 'POST':
        message = Message.objects.create(
            user=request.user,
            room=room,
            body=body
        )
        room.participants.add(request.user)
        return redirect('room', pk=room.id)
    context = {'room':room, 'msgs':msgs, 'participants' : participants}
    return render(request, 'base/room.html',context)

# Private View
@login_required(login_url="/login/")
def userProfile(request, pk):
    user = User.objects.get(id=pk)
    rooms = user.room_set.all()
    room_message = user.message_set.all()
    topics = Topic.objects.all()
    context = {'user':user, 'rooms':rooms, 'room_message':room_message, 'topics':topics}
    return render(request, 'base/profile.html', context)

@login_required(login_url="/login/")
def updateProfile(request):
    user = request.user
    form = UserForm(instance=user) 
    if request.method == 'POST':
        form = UserForm(request.POST,  instance=user) 
        if form.is_valid():
            form.save()
            return redirect('profile', pk=user.id)
    context = {'form': form}
    return render(request, 'base/update_user.html', context)

@login_required(login_url="/login/")
def create_room(request):
    form = RoomForm()
    if request.method  == "POST" :
        form = RoomForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    context = {'form':form}
    return render(request, 'base/room_form.html', context)

@login_required(login_url="/login/")
def update_room(request, pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)

    if request.user != room.host:
        return HttpResponse('You are not allowed here!!')

    if request.method  == "POST" :
        form = RoomForm(request.POST, instance=room)
        if form.is_valid() :
            form.save()
            return redirect('home')
    context = {'form':form}
    return render(request, 'base/room_form.html', context)

@login_required(login_url="/login/")
def delete_room(request, pk):
    room = get_object_or_404(Room, id=pk)

    if request.user != room.host:
        return HttpResponse('You are not allowed here!!')

    if request.method  == "POST" :
        room.delete()
        return redirect('home')
    context = {'obj':room}
    return render(request, 'base/delete.html', context)

@login_required(login_url="/login/")
def delete_message(request, pk):
    message = get_object_or_404(Message, id=pk)

    if request.user != message.user:
        return HttpResponse('You are not allowed here!!')

    if request.method  == "POST" :
        message.delete()
        return redirect('home')
    context = {'obj':message}
    return render(request, 'base/delete.html', context)
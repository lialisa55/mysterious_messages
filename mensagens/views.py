from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.utils import timezone
from django.contrib import messages
from .models import Room, Message

# Página inicial com lista de salas
# Página inicial com lista de salas
@login_required
def home(request):
    rooms = Room.objects.all()
    return render(request, 'mensagens/home.html', {'rooms': rooms})

# Página de sala com as mensagens
@login_required
def room(request, room_id):
    room = get_object_or_404(Room, id=room_id)
    messages = Message.objects.filter(room=room).order_by('timestamp')
    return render(request, 'mensagens/room.html', {'room': room, 'messages': messages})

# Registro de usuário
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'mensagens/register.html', {'form': form})


@login_required
def profile(request):
    return render(request, 'mensagens/profile.html')

# Login de usuário
def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Credenciais inválidas')
    return render(request, 'mensagens/login.html')

def send_message(request, room_id):
    if request.method == 'POST':
        room = get_object_or_404(Room, id=room_id)
        content = request.POST.get('content')
        if content:
            Message.objects.create(
                room=room,
                sender=request.user,
                content=content,
                timestamp=timezone.now()
            )
        return redirect('room', room_id=room.id)
    
@login_required
def create_room(request):
    if request.method == "POST":
        room_name = request.POST.get('name')
        if room_name:
            room = Room(name=room_name)
            room.save()
            room.participants.add(request.user)  # Adiciona o usuário como participante
            return redirect('room_detail', room_id=room.id)  # Redireciona para a sala recém-criada
    return render(request, 'mensagens/create_room.html')
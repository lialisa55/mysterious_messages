from django.db import models
from django.contrib.auth.models import User

# Modelo do Jogador (extende o usuário padrão do Django)
class PlayerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nickname = models.CharField(max_length=50)
    score = models.IntegerField(default=0)
    last_login = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nickname

# Modelo da Sala (representa um canal ou grupo colaborativo)
class Room(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    participants = models.ManyToManyField(PlayerProfile, related_name='rooms')

    def __str__(self):
        return self.name

# Modelo das Mensagens (envios entre jogadores dentro de uma sala)
class Message(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(PlayerProfile, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_clue = models.BooleanField(default=False)  # Indica se a mensagem é uma "pista" no jogo

    def __str__(self):
        return f"{self.sender.nickname} in {self.room.name}: {self.content[:20]}"

# Modelo de Progresso de Jogo
class GameProgress(models.Model):
    player = models.ForeignKey(PlayerProfile, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    current_level = models.IntegerField(default=1)
    clues_found = models.IntegerField(default=0)
    is_completed = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.player.nickname} progress in {self.room.name}"

# Modelo de Evento (eventos dinâmicos na sala, como sustos ou missões)
class Event(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='events')
    description = models.CharField(max_length=200)
    triggered_at = models.DateTimeField()
    is_resolved = models.BooleanField(default=False)

    def __str__(self):
        return f"Event in {self.room.name}: {self.description}"


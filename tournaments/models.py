from django.utils import timezone
from django.db import models
from django.contrib.auth.models import User
from main.models import Level, VideoGame
from users.models import Players

# Tabla de los torneos
class Tournament(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    creator = models.ForeignKey(User,on_delete=models.DO_NOTHING, related_name="Creator",default=0)
    date = models.DateTimeField()
    status = models.IntegerField(default=0)
    players = models.IntegerField(default=0)
    max_players = models.IntegerField(default=0)
    rounds = models.IntegerField(default=0)
    round = models.IntegerField(default=0)
    min_level = models.ForeignKey(Level, on_delete=models.DO_NOTHING,related_name="level")
    game = models.ForeignKey(VideoGame, on_delete=models.DO_NOTHING, related_name="videogame")
    tournament_winner = models.ForeignKey(Players, on_delete=models.DO_NOTHING, related_name="tournament_winner", default=0)
    
    def __str__(self):
        return f"{self.id} - {self.name}"
    
# Tabla que se guardará el registro de las partidas
class Game(models.Model):
    tournament = models.ForeignKey(Tournament, on_delete=models.DO_NOTHING, related_name="tournament")
    round = models.IntegerField(default=0)
    player1 = models.ForeignKey(Players, related_name='player1', on_delete=models.DO_NOTHING)
    player2 = models.ForeignKey(Players, related_name='player2', on_delete=models.DO_NOTHING)
    result_player1 = models.IntegerField(default=0)
    result_player2 = models.IntegerField(default=0)
    winner = models.ForeignKey(Players, related_name='game_winner', on_delete=models.DO_NOTHING)
    date = models.DateTimeField(default=timezone.now)
    status = models.IntegerField(default=0)

    def __str__(self):
        return f"Game {self.id} - {self.tournament.name} - Round: {self.round} - {self.player1.username} vs {self.player2.username}"  

# Tablas auxiliares para los torneos
# Tabla que recogera de manera temporal la informacion de los jugadores que participen en torneos
class PlayersTournament(models.Model):
    tournament = models.ForeignKey(Tournament, on_delete=models.DO_NOTHING, related_name="tournament_player",default=1)
    player = models.ForeignKey(Players, on_delete=models.DO_NOTHING, related_name="player_tournament",default=1)
    win = models.IntegerField(default=0)
    draw = models.IntegerField(default=0)
    lose = models.IntegerField(default=0)
    points = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.tournament.name} - {self.player.username} - Points: {self.points}"

# Tabla que se guardara y borrara los registros de los jugadores que han enviado como resultado de su partida y confirmar que la información enviada es igual y coerente
class GameAux(models.Model):
    tournament = models.ForeignKey(Tournament, on_delete=models.DO_NOTHING, related_name="tournament_aux")
    round = models.IntegerField(default=0)
    player1 = models.ForeignKey(Players, related_name='player1_aux', on_delete=models.DO_NOTHING)
    player2 = models.ForeignKey(Players, related_name='player2_aux', on_delete=models.DO_NOTHING)
    result_player1 = models.IntegerField(default=0)
    result_player2 = models.IntegerField(default=0)
    winner = models.ForeignKey(Players, related_name='game_winner_aux', on_delete=models.DO_NOTHING)
    date = models.DateTimeField(default=timezone.now)
    player_sender = models.ForeignKey(User, related_name='user_sender', on_delete=models.DO_NOTHING,default=1)

    def __str__(self):
        return f"Game {self.id}"
    
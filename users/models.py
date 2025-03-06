from django.db import models
from main.models import Level

# Create your models here.
class Players(models.Model):
    username = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    level = models.ForeignKey(Level, on_delete=models.DO_NOTHING)
    tournament = models.IntegerField(default=0)
    tournament_played = models.IntegerField(default=0)
    tournament_wins = models.IntegerField(default=0)
    games_played = models.IntegerField(default=0)
    games_wins = models.IntegerField(default=0)
    games_loses = models.IntegerField(default=0)
    games_draws = models.IntegerField(default=0)
    winrate = models.FloatField(default=0)
    
    def __str__(self):
        return f"{self.id} - {self.username} - {self.email} - {self.level.name} - {self.tournament} - {self.tournament_played} - {self.tournament_wins} - {self.games_played} - {self.games_wins} - {self.games_loses} - {self.games_draws} - {self.winrate}"
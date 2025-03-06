from django.contrib import admin
from .models import Tournament, Game, PlayersTournament, GameAux

# Register your models here.
admin.site.register(Tournament)
admin.site.register(Game)
admin.site.register(PlayersTournament)
admin.site.register(GameAux)
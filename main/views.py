from django.shortcuts import render
from .models import *
from users.models import Players

# Pagina de Inicio
def index(request):
    return render(request, 'index.html')

# Pagina de los rankings
def rankings(request):
    if request.method == 'GET':
        players = Players.objects.all()
        players_tournaments = players.order_by("-tournament_wins")[:5]
        players_winrate = players.order_by("-winrate")[:5]
        players_participations = players.order_by("-tournament_played")[:5]
        return render(request, 'rankings.html',{
            'pt': players_tournaments,
            'pw': players_winrate,
            'pp' : players_participations
        })
    else:
        return render(request, 'rankings.html')
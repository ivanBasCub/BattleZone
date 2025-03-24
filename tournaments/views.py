from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from main.models import *
from users.models import *
from .models import *

# Pagina de los torneos
def tournaments(request):
    if(request.user.is_anonymous):
        return redirect('signup')
    
    elif request.user.is_staff:
        tournaments = Tournament.objects.all()
        player = Players.objects.all()

        return render(request, 'list_tournament.html', {
            'tournaments': tournaments,
            'player': player
        })
    else:
        player = Players.objects.get(username=request.user.username)
        tournaments = Tournament.objects.filter(min_level = player.level, status = 0)

        return render(request, 'list_tournament.html', {
            'tournaments': tournaments,
            'player': player
        })
    
# Registro de un torneo
@login_required
def join_tournament(request):
    if request.method == 'GET':
        return redirect('tournament')
    else:
        player = Players.objects.get(username=request.user.username)
        if(player.tournament == 0):
            tournament = Tournament.objects.get(id=request.POST["tournament_id"])
            tournament.players += 1
            player.tournament = tournament.id
            tournament.save()
            player.save()

            return redirect('tournament')
        else:
            tournament_old = Tournament.objects.get(id=player.tournament)
            tournament_old.players -= 1
            tournament_old.save()

            tournament = Tournament.objects.get(id=request.POST["tournament_id"])
            tournament.players += 1
            player.tournament = tournament.id
            tournament.save()
            player.save()

            return redirect('tournament')

# Salir de un torneo
@login_required
def leave_tournament(request):
    if request.method == 'GET':
        return redirect('tournament')
    else:
        player = Players.objects.get(username=request.user.username)
        tournament = Tournament.objects.get(id=player.tournament)
        tournament.players -= 1
        player.tournament = 0
        tournament.save()
        player.save()

        return redirect('tournament')

# Crear un torneo por un administrador
@login_required
def create_tournament(request):
    if request.user.is_staff:
        if request.method == 'GET':
            videogames = VideoGame.objects.all()
            levels = Level.objects.all()
            return render(request, 'create_tournament.html',{
                'videogames': videogames,
                'levels': levels
            })
        else:
            videogame = VideoGame.objects.get(id=request.POST["videogame"])
            level = Level.objects.get(id=request.POST["level"])
            player = Players.objects.get(username = "no_winner")
            tournament = Tournament(name = request.POST["title"], description = request.POST["description"], creator= request.user, date = request.POST["date"], max_players = request.POST["players"], min_level = level, game = videogame, tournament_winner = player,status = 0, round = 0, rounds = request.POST["round"])
            tournament.save()
            return redirect('tournament')
    else:
        return redirect('index')
    
# Borrar un torneo por un administrador
@login_required
def delete_tournament(request):
    if request.user.is_staff:
        t = Tournament.objects.get(id=request.POST["tournament_id"])
        list_players = Players.objects.filter(tournament = request.POST["tournament_id"])
        player = PlayersTournament.objects.filter(tournament = t)
        
        for player in list_players:
            player.tournament = 0
            player.save()

        player.delete()
        t.delete()
        return redirect('home')
    else:
        return redirect('index')

# Pagina que nos mostrara la clasificación del usuario y contra quien le toca. En el caso del administrador la creacion de los partidos de manera aleatoria y comprueba los resultados enviados por los alumnos
@login_required
def playMatch(request):
    if request.user.is_anonymous:
        return redirect('signup')
    else:
        t = Tournament.objects.get(id = request.POST["tournament_id"])

        if request.user.is_staff:
            # En el caso de que el torneo no haya empezado
            if t.status == 0:
                startTournament(t)

            # Obtenemos todos los datos necesarios para que la página pueda funcionar 
                # Obtenemos la lista de los jugadores y los ordenamos segun los puntos que tengan
            players = PlayersTournament.objects.filter(tournament = t).order_by("-points")
                # Recogemos la lista de los juegos de la ronda que toca jugar
            list_games = Game.objects.filter(tournament = t, round = t.round)
                # Recogemos la lista de los juegos que han sido enviados por los jugadores
            list_games_aux = GameAux.objects.filter(tournament = t, round = t.round)

            
            # Comprobamos que las listas no esten vacias y si es el caso se le indica su valor como None
            if len(list_games_aux) == 0:
                list_games_aux = None
            
            if len(list_games) == 0:
                list_games = None

            # Preguntamos si han dado al boton de crear los partidos 
            if request.POST.get("create") == "create" and t.round < t.rounds:
                # Creamos los partidos
                createMatchs(t, players)
                # Actualizamos la lista de los partidos
                list_games = Game.objects.filter(tournament = t, round = t.round)
            
            # Cuando el administrador envie el resultado final
            if request.POST.get("final_result") == "result" :
                game = Game.objects.get(id = request.POST["game_id"])
                if game.status == 0:
                    sendResult(request, t, game)
                    list_games = Game.objects.filter(tournament = t, round = t.round)

            # Aqui llamamos a la funcion cuando se cumpla las condiciones indicadas
            if t.round >= t.rounds and request.POST.get("final") == "final":
                if players[0].points != players[1].points:
                    winnerTournament(t, players)
                    return redirect("index")
                else:
                    extraRound(t, players)

            # Renderizamos todos los datos necesitamos
            return render(request, "tournament.html", {
                "tournament": t,
                "list_players": players,
                "list_games" : list_games,
                "list_games_aux" : list_games_aux
            })
        
        else:
            player = Players.objects.get(username = request.user.username)
            user = User.objects.get(username = request.user.username)
            list_players = PlayersTournament.objects.filter(tournament = t).order_by("-points")
            games = Game.objects.filter(player1 = player,tournament = t,round = t.round) | Game.objects.filter(player2 = player,tournament = t,round = t.round)
            list_games = GameAux.objects.filter(player_sender = user,tournament = t,round = t.round)
            game = None 
            
            for prueba in games:
                game = prueba
   
            if request.POST.get("result") == "result":
                aux_game = GameAux.objects.create(tournament = t, round = t.round, player_sender = user, player1 = game.player1, player2 = game.player2, result_player1 = request.POST["result_player1"], result_player2 = request.POST["result_player2"], winner = game.winner)
                aux_game.save()

            if len(list_games) == 0:
                list_games = None

            if(list_games != None):
                game = None 
                return render(request, "tournament.html",{
                    "tournament" : t,
                    "list_players" : list_players,
                    "game" : game,
                    "status": 1
                })

            else:
                return render(request, "tournament.html",{
                    "tournament" : t,
                    "list_players" : list_players,
                    "game" : game,
                    "status": 0
                })
            
# Función para actualizar el estado de un torneo que recien a empezado
def startTournament(t):
    # Cambiamos el estado del torneo
    t.status = 1
    t.save()
                
    # Obtenemos los jugadores que participan en el torneo
    list_players = Players.objects.filter(tournament = t.id)

    # Los guardamos en una tabla temporal
    for player in list_players:
        pt = PlayersTournament.objects.create(tournament = t, player = player)
        pt.save()

# Pagina que crea los partidos de manera "aleatoria"
def createMatchs(t, list_players):
    # Obtenemos el torneo y la lista de jugadores
    list_games = Game.objects.filter(tournament = t)

    if len(list_games) != 0:
        t.round += 1
        t.save()
    else:
        t.round = 1
        t.save()
    
    # Creamos los partidos
    for i in range(0,len(list_players),2):
        game = Game.objects.create(tournament = t, round = t.round, player1 = list_players[i].player, player2 = list_players[i+1].player, winner = Players.objects.get(username = "no_winner"))
        game.save()

# Funcion que nos permite enviar los resultados de los partidos
def sendResult(request, t, game):
    # Recogemos los datos de los jugadores del formulario
    player1 = PlayersTournament.objects.get(player = request.POST["player1"], tournament = t)
    player2 = PlayersTournament.objects.get(player = request.POST["player2"], tournament = t)
    result_player1 = request.POST["result_player1"]
    result_player2 = request.POST["result_player2"]

    # Comprobamos quien ha ganado y le asignamos los puntos
    if result_player1 > result_player2:
        player1.win += 1
        player2.lose += 1
        player1.points += 3
        player_winner = Players.objects.get(id = player1.player.id)
        game.winner = player_winner
    elif result_player1 < result_player2:
        player2.win += 1
        player1.lose += 1
        player2.points += 3
        player_winner = Players.objects.get(id = player2.player.id)
        game.winner = player_winner
    else:
        player1.draw += 1
        player2.draw += 1
        player1.points += 1
        player2.points += 1

    game.result_player1 = result_player1
    game.result_player2 = result_player2
    game.status = 1
    game.save()

    # Borramos los reportes de los jugadores
    user1 = User.objects.get(username = player1.player.username)
    user2 = User.objects.get(username = player2.player.username)
    del_games = GameAux.objects.filter(tournament = t, player_sender = user1, round = t.round) | GameAux.objects.filter(tournament = t, player_sender = user2, round = t.round)
    del_games.delete() 
    player1.save()
    player2.save()

# Función en el caso de empate en el primer puesto
def extraRound(t,list_players):
    # Actualizamos el torneo con una ronda mas
    t.round += 1
    t.save()

    # Creamos el partido del desempate
    game = Game.objects.create(tournament = t, round = t.round, player1 = list_players[0].player, player2 = list_players[1].player, winner = Players.objects.get(username = "no_winner"))
    game.save()

# Funcion para indicar quien es ganador del torneo y finalizar el torneo
def winnerTournament(t, list_players):
    # Indicamos quien es jugador ganador del torneo y actualizamos el estado del torneo
    player_winner = Players.objects.get(id = list_players[0].player.id)
    player_winner.tournament_wins += 1
    player_winner.save()

    t.tournament_winner = player_winner
    t.status = 2
    t.save()

    # Actualizamos los datos de los jugadores que han participado en la tabla final
    for auxplayer in list_players:
        player = Players.objects.get(id = auxplayer.player.id)
        total_games = auxplayer.win + auxplayer.draw + auxplayer.lose
        player.tournament_played += 1
        player.games_played += total_games
        player.games_wins += auxplayer.win
        player.games_loses += auxplayer.lose
        player.games_draws += auxplayer.draw
        winrate = (player.games_wins / player.games_played) * 100
        player.winrate = round(winrate,2)
        player.tournament = 0
        player.save()
        auxplayer.delete()
    
# Pagina en la cual los jugadores envian los resultados de los partidos
@login_required
def match(request):
    if request.user.is_anonymous:
        return redirect('signup')
    else:
        t = Tournament.objects.get(id = request.POST["tournament_id"])
        game = Game.objects.get(id = request.POST["game_id"])
        
        return render(request, "match.html",{
            "tournament" : t,
            "game" : game
        })
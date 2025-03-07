from django.shortcuts import render, redirect
from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required
from .models import *
from main.models import *
from tournaments.models import *
from django.utils import timezone

# Pagina de Creación de Cuenta
def signup(request):
    if request.method == 'GET':
        return render(request, 'signup.html')
    else:
        if request.POST["password1"] == request.POST["password2"]:
                try:
                    user = User.objects.create_user(username=request.POST["username"], email=request.POST["email"] , password=request.POST["password1"])
                    level = Level.objects.get(id=request.POST["level"])
                    player = Players(username=request.POST["username"], email=request.POST["email"], level = level)
                    player.save()
                    user.save()
                    login(request, user)
                    return redirect('index')
                except IntegrityError:
                    return render(request, 'signup.html',{
                        'msg': "The user already exists"
                    })
        else:
            return render(request, 'signup.html',{
                'msg': "The passwords do not match"
            })
        
# Pagina de Inicio de Sesión
def signin(request):
    if request.method == 'GET':
        return render(request, 'signin.html')
    else:
        user = authenticate(request, username=request.POST["username"], password=request.POST["password"])
        if user is None:
            return render(request, 'signin.html',{
                'msg': "The username or password is incorrect"
            })
        else:
            login(request, user)
            return redirect('home')   

# Pagina de Cierre de Sesión
@login_required
def signout(request):
    logout(request)
    return redirect('index')

# Pagina de Perfil de Usuario
@login_required
def home(request):
    if request.method == 'GET':
        if request.user.is_staff:
            tournament = Tournament.objects.filter(creator = request.user).values()
            now = timezone.now()
            return render(request, 'home.html',{
                "tournaments" : tournament,
                "now": now
            })
        else:
            player = Players.objects.get(username=request.user.username)
            draw_case = Players.objects.get(username = "no_winner")
            if(player.tournament != 0):
                tournament = Tournament.objects.get(id=player.tournament)
            else:
                tournament = None
                    
            games = Game.objects.filter(player1=player.id) | Game.objects.filter(player2=player.id)
            games = games.order_by('-date')[:5]
            videogames = VideoGame.objects.all()

            return render(request, 'home.html',{
                'player': player,
                'tournament': tournament,
                'games': games,
                'videogames': videogames,
                'draw_case' : draw_case
            })
    else:
        return render(request, 'home.html')
    
# Pagina para Editar Perfil de Usuario
@login_required
def update_user(request):
    if request.method == "POST":
        player = Players.objects.get(username = request.user.username)
        user = User.objects.get(username=request.user.username)
        if request.POST["username"] != player.username:
            user.username = request.POST["username"]
            player.username = request.POST["username"]

        if request.POST["email"] != player.email:
            user.email = request.POST["email"]
            player.email = request.POST["email"]

        if request.POST["password1"] != "":
            if request.POST["password1"] == request.POST["password2"]:
                user.set_password(request.POST["password1"])

        player.save()
        user.save()
        if request.POST["password1"] != "":
            return redirect("signin")
        else:
            return redirect("home")
    else:
        return render(request, 'update_user.html')


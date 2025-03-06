"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from main import views as main_views
from users import views as users_views
from tournaments import views as tournaments_views

urlpatterns = [
    path('admin/', admin.site.urls),
    # Vistas de la aplicacion main
    path('', main_views.index, name='index'),
    path('rankings/', main_views.rankings, name='rankings'),
    
    # Vistas de la aplicacion users
    path('signup/', users_views.signup, name='signup'),
    path('signin/', users_views.signin, name='signin'),
    path('signout/', users_views.signout, name='signout'),
    path('update_user/', users_views.update_user, name='update_user'),
    path('home/', users_views.home, name='home'),

    # Vistas de la aplicacion tournaments
    path('tournament/', tournaments_views.tournaments, name='tournament'),
    path('join_tournament/', tournaments_views.join_tournament, name='join_tournament'),
    path('leave_tournament/', tournaments_views.leave_tournament, name='leave_tournament'),
    path('create_tournament/', tournaments_views.create_tournament, name='create_tournament'),
    path('delete_tournament/', tournaments_views.delete_tournament, name='delete_tournament'),
    path("match/", tournaments_views.match, name="match"),
    path('play/',tournaments_views.playMatch, name="play")
]

from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import Movie
import requests

# Create your views here.
@login_required
def home(request):
    response = requests.get("https://omdbapi.com/?apikey=38b4b85b&s=Batman&type=movie")
    results_json = response.json()
    movies = results_json["Search"]
    context = {
        "movies": movies
    }
    return render(request, "index.html", context)

@login_required
def home2(request):
    movies = Movie.objects.all()
    return render(request,"home.html",{"movies": movies})

def create_user(request):
    if request.method == "POST":
        user = User.objects.create_user(
            username=request.POST["username"],
            email=request.POST["email"],
            password=request.POST["password"],
        )
        user.save()
        return redirect("/users/login/")
    return render(request, "registro.html")

def login_user(request):
    if request.method == "POST":
        user = authenticate(request, username=request.POST["username"], password=request.POST["password"])
        if user:
            login(request, user)
            return redirect("/")
        return render(request, "login.html", {"error_message": "Usuário não existe"})
    return render(request, "login.html")

def logout_user(request):
    logout(request)
    return redirect("/users/login/")

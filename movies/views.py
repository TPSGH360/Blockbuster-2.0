from rest_framework import viewsets
from .models import Movie
from .serializers import MovieSerializer
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.contrib import messages
from django.db.models import Q
from customers.models import CustomerProfile
from django.contrib.auth.decorators import user_passes_test
from .forms import MovieForm


# API ViewSet for Movie Model
class MovieViewSet(viewsets.ModelViewSet):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer


# Home View - Display and Search Movies
def home(request):
    query = request.GET.get("q")
    if query:
        movies = Movie.objects.filter(
            Q(title__icontains=query)
            | Q(director__icontains=query)
            | Q(genre__icontains=query)
        )
    else:
        movies = Movie.objects.all()
    return render(request, "movies/index.html", {"movies": movies})


# Register View - User Registration
def register(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")
        age = request.POST.get("age")
        city = request.POST.get("city")
        phone_number = request.POST.get("phone_number")

        # Validate passwords
        if password1 != password2:
            messages.error(request, "Passwords do not match.")
            return redirect("register")

        # Create the user
        if not User.objects.filter(username=username).exists():
            user = User.objects.create_user(
                username=username, email=email, password=password1
            )
            CustomerProfile.objects.create(
                user=user, age=age, city=city, phone_number=phone_number
            )
            login(request, user)
            messages.success(request, "Registration successful. Welcome!")
            return redirect("/")
        else:
            messages.error(request, "Username already exists.")
            return redirect("register")

    return render(request, "movies/register.html")


# Add Movie View - Admin Only Functionality
@user_passes_test(lambda u: u.is_staff or u.is_superuser)
def add_movie(request):
    if request.method == "POST":
        form = MovieForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Movie added successfully!")
            return redirect("/")
    else:
        form = MovieForm()

    return render(request, "movies/add_movie.html", {"form": form})


# Edit Movie View - Admin Only Functionality
@user_passes_test(lambda u: u.is_staff or u.is_superuser)
def edit_movie(request, movie_id):
    movie = get_object_or_404(Movie, id=movie_id)

    if request.method == "POST":
        form = MovieForm(request.POST, instance=movie)
        if form.is_valid():
            form.save()
            messages.success(request, "Movie updated successfully!")
            return redirect("/")
    else:
        form = MovieForm(instance=movie)

    return render(request, "movies/edit_movie.html", {"form": form, "movie": movie})


# Delete Movie View - Admin Only Functionality
@user_passes_test(lambda u: u.is_staff or u.is_superuser)
def delete_movie(request, movie_id):
    movie = get_object_or_404(Movie, id=movie_id)
    movie.delete()
    messages.success(request, f"The movie '{movie.title}' has been removed.")
    return redirect("/")

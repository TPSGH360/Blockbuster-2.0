from django.contrib import admin
from .models import Movie


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ("title", "director", "year_released", "is_available")
    fields = ("title", "director", "year_released", "genre", "is_available", "photo")

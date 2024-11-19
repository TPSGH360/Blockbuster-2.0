from django.db import models


class Movie(models.Model):
    title = models.CharField(max_length=255)
    director = models.CharField(max_length=255)
    year_released = models.IntegerField()
    genre = models.CharField(max_length=100)
    is_available = models.BooleanField(default=True)
    photo = models.ImageField(upload_to="movie_photos/", null=True, blank=True)

    def __str__(self):
        return self.title

from datetime import date
from django.db import models
from django.contrib.auth.models import User
from movies.models import Movie


class Loan(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    loan_date = models.DateField(auto_now_add=True)
    return_date = models.DateField(null=True, blank=True)
    is_active = models.BooleanField(default=True)

    def is_late(self):
        return date.today() > self.return_date

    def __str__(self):
        return f"Loan: {self.customer.username} - {self.movie.title}"

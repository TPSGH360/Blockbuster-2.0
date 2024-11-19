from rest_framework import serializers
from .models import Loan
from movies.serializers import MovieSerializer
from django.contrib.auth.models import User


class LoanSerializer(serializers.ModelSerializer):
    movie = MovieSerializer(read_only=True)
    customer = serializers.StringRelatedField()

    class Meta:
        model = Loan
        fields = ["id", "customer", "movie", "loan_date", "return_date", "is_active"]

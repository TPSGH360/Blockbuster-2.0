from datetime import date
from .models import Loan
from .serializers import LoanSerializer
from movies.models import Movie
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test, login_required
from django.shortcuts import get_object_or_404, redirect, render


class LoanViewSet(viewsets.ModelViewSet):
    queryset = Loan.objects.all()
    serializer_class = LoanSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Loan.objects.all()
        return Loan.objects.filter(customer=user)


# 1. Monitor Loans - Admin/Staff Only
@user_passes_test(lambda u: u.is_staff or u.is_superuser)
def monitor_loans(request):
    loans = Loan.objects.all()
    if request.method == "POST":
        loan_id = request.POST.get("loan_id")
        loan = get_object_or_404(Loan, id=loan_id)
        loan.is_active = False
        loan.save()
        if loan.return_date < date.today():
            loan.customer.is_active = False
            loan.customer.save()
            messages.error(
                request,
                f"Membership for '{loan.customer.username}' has been revoked due to late return.",
            )
        else:
            messages.success(
                request, f"Loan for '{loan.movie.title}' has been marked as completed."
            )
        return redirect("/loans/monitor/")
    return render(request, "loans/monitor_loans.html", {"loans": loans})


# 2. User Loans - Display User-Specific Loans
@login_required
def user_loans(request):
    loans = Loan.objects.filter(customer=request.user)
    return render(request, "loans/user_loans.html", {"loans": loans})


# 3. Loan Movie - For Users to Borrow a Movie
@login_required
def loan_movie(request, movie_id):
    if (
        not hasattr(request.user, "customer_profile")
        or not request.user.customer_profile.is_active
    ):
        messages.error(request, "Your account is inactive. Contact admin for support.")
        return redirect("/")

    movie = get_object_or_404(Movie, id=movie_id, is_available=True)

    if request.method == "POST":
        return_date = request.POST.get("return_date")
        if return_date:
            Loan.objects.create(
                customer=request.user, movie=movie, return_date=return_date
            )
            messages.success(
                request,
                f"You have successfully borrowed '{movie.title}'. Please return it by {return_date}.",
            )
            return redirect("/")
    return render(request, "movies/loan_movie.html", {"movie": movie})


# 4. Complete Loan - Admin/Staff Mark Loan as Completed
@user_passes_test(lambda u: u.is_staff or u.is_superuser)
def complete_loan(request, loan_id):
    loan = get_object_or_404(Loan, id=loan_id)
    loan.is_active = False
    loan.save()
    messages.success(
        request, f"Loan for '{loan.movie.title}' has been marked as completed."
    )
    return redirect("/loans/monitor/")


# 5. Return Movie - User Returning a Movie On-Time
@login_required
def return_movie(request, loan_id):
    loan = get_object_or_404(Loan, id=loan_id, customer=request.user)

    if loan.return_date < date.today():
        messages.error(request, "You are late. Contact admin to complete the loan.")
    else:
        loan.is_active = False
        loan.save()
        messages.success(
            request, f"You have successfully returned '{loan.movie.title}'."
        )
    return redirect("/loans/")

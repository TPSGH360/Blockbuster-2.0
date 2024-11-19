from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import CustomerProfile
from .serializers import UserSerializer, CustomerProfileSerializer
from django.shortcuts import render, redirect, get_object_or_404


# API ViewSet for User Model
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


# API ViewSet for CustomerProfile Model
class CustomerProfileViewSet(viewsets.ModelViewSet):
    queryset = CustomerProfile.objects.all()
    serializer_class = CustomerProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return CustomerProfile.objects.all()
        return CustomerProfile.objects.filter(user=user)


# Edit User Profile View - User Functionality
@login_required
def edit_profile(request):
    try:
        customer_profile = CustomerProfile.objects.get(user=request.user)
    except CustomerProfile.DoesNotExist:
        messages.error(request, "Customer profile not found.")
        return redirect("/")

    if request.method == "POST":
        customer_profile.city = request.POST.get("city")
        customer_profile.phone_number = request.POST.get("phone_number")
        customer_profile.age = request.POST.get("age")
        customer_profile.save()
        messages.success(request, "Your profile has been updated!")
        return redirect("/customers/")

    return render(request, "movies/edit_profile.html", {"profile": customer_profile})


# Customer List View - Admin Only Functionality
@user_passes_test(lambda u: u.is_staff or u.is_superuser)
def customer_list(request):
    customers = CustomerProfile.objects.all()
    return render(request, "customers/customer_list.html", {"customers": customers})


# Edit Customer View - Admin Only Functionality
@user_passes_test(lambda u: u.is_staff or u.is_superuser)
def edit_customer(request, customer_id):
    customer = get_object_or_404(CustomerProfile, id=customer_id)

    if request.method == "POST":
        customer.city = request.POST.get("city")
        customer.phone_number = request.POST.get("phone_number")
        customer.age = request.POST.get("age")
        customer.save()
        messages.success(request, "Customer details updated successfully!")
        return redirect("/customers/list/")

    return render(request, "customers/edit_customer.html", {"customer": customer})


# Toggle Customer Status View - Admin Only Functionality
@user_passes_test(lambda u: u.is_staff or u.is_superuser)
def toggle_customer_status(request, customer_id):
    customer = get_object_or_404(CustomerProfile, id=customer_id)

    if request.method == "POST":
        customer.is_active = not customer.is_active
        customer.save()
        messages.success(
            request,
            f"Customer has been {'activated' if customer.is_active else 'deactivated'}.",
        )
        return redirect("/customers/list/")

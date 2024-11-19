from rest_framework.routers import DefaultRouter
from django.contrib import admin
from django.urls import path, include
from customers.views import (
    UserViewSet,
    CustomerProfileViewSet,
    customer_list,
    edit_customer,
    edit_profile,
    toggle_customer_status,
)
from movies import views
from movies.views import MovieViewSet, add_movie, delete_movie, edit_movie, register
from loans.views import (
    LoanViewSet,
    complete_loan,
    loan_movie,
    monitor_loans,
    return_movie,
    user_loans,
)
from django.views.generic import TemplateView
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static


router = DefaultRouter()
router.register("users", UserViewSet)
router.register("customers", CustomerProfileViewSet, basename="customer")
router.register("movies", MovieViewSet, basename="movie")
router.register("loans", LoanViewSet, basename="loan")

urlpatterns = [
    path("", views.home, name="home"),
    path("admin/", admin.site.urls),
    path("api/", include(router.urls)),
    path("movies/", TemplateView.as_view(template_name="movies/index.html")),
    path("loans/", user_loans, name="user_loans"),
    path("customers/", TemplateView.as_view(template_name="customers/index.html")),
    path(
        "login/",
        auth_views.LoginView.as_view(template_name="movies/login.html"),
        name="login",
    ),
    path("logout/", auth_views.LogoutView.as_view(next_page="/"), name="logout"),
    path("register/", register, name="register"),
    path("customers/edit_profile/", edit_profile, name="edit_profile"),
    path("customers/list/", customer_list, name="customer_list"),
    path("loans/monitor/", monitor_loans, name="monitor_loans"),
    path("customers/edit/<int:customer_id>/", edit_customer, name="edit_customer"),
    path(
        "customers/toggle/<int:customer_id>/",
        toggle_customer_status,
        name="toggle_customer_status",
    ),
    path("movies/add/", add_movie, name="add_movie"),
    path("movies/edit/<int:movie_id>/", edit_movie, name="edit_movie"),
    path("movies/delete/<int:movie_id>/", delete_movie, name="delete_movie"),
    path("movies/loan/<int:movie_id>/", loan_movie, name="loan_movie"),
    path("movies/return/<int:loan_id>/", return_movie, name="return_movie"),
    path("movies/complete/<int:loan_id>/", complete_loan, name="complete_loan"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

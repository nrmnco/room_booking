from django.urls import include, path
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework.routers import DefaultRouter

from .views import BookingViewSet, UserRegistrationView

router = DefaultRouter()
router.register(r"bookings", BookingViewSet, basename="booking")

urlpatterns = [
    path("register/", UserRegistrationView.as_view(), name="register"),
    path("login/", obtain_auth_token, name="login"),
    path("", include(router.urls)),
]

from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import AddressViewSet, LoginView, ProfileView, RegisterView


router = DefaultRouter()
router.register('addresses', AddressViewSet, basename='address')

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('', include(router.urls)),
]

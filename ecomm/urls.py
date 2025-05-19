
from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
# urlpatterns = [
#     path('',views.home, name='home'),
#     path('contact/',views.Contact, name='contact'),
# ]

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('contact/',views.ContactView.as_view(), name='contact'),  # ✅ Corrected
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('accounts/login/', auth_views.LoginView.as_view(), name='login'),
]

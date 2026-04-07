from django.urls import path
from . import views

urlpatterns = [
    path('', views.home),
    path('add/', views.add_schedule),
    path('login/', views.login_view),
    path('signup/', views.signup_view),
    path('logout/', views.logout_view),
    path('friends/', views.coming),
    path('settings/', views.coming),
]
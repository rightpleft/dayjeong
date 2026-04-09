from django.urls import path
from . import views

urlpatterns = [
    path('', views.home),
    path('add/', views.add_schedule),
    path('login/', views.login_view),
    path('signup/', views.signup_view),
    path('logout/', views.logout_view),
    path('settings/', views.coming),
    path('friends/', views.friends),
    path('add-friend/', views.send_request),
    path('friends/', views.friends),
    path('send-request/', views.send_request),
    path('requests/', views.friend_requests),
    path('accept/<int:id>/', views.accept_request),
    path('reject/<int:id>/', views.reject_request),
]
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
    path('add-friend/', views.add_friend),
    path('delete-friend/<int:id>/', views.delete_friend),
    path('block-friend/<int:id>/', views.block_friend),
    path('friend/<int:user_id>/', views.friend_calendar),
]
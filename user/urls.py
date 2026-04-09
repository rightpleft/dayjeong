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
     path('friend/<int:user_id>/', views.friend_calendar),

    path('send-schedule-request/', views.send_schedule_request),

    path('schedule-requests/', views.schedule_requests),
    path('accept-schedule/<int:id>/', views.accept_schedule),
    path('reject-schedule/<int:id>/', views.reject_schedule),
]
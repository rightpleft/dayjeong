from django.urls import path
from . import views

urlpatterns = [

    # 🏠 메인 페이지
    path('', views.home),

    # 📅 일정 추가 / 목록 페이지
    path('add/', views.add_schedule),

    # 🔐 인증 관련
    path('login/', views.login_view),      # 로그인
    path('signup/', views.signup_view),    # 회원가입
    path('logout/', views.logout_view),    # 로그아웃

    # ⚙️ 설정 (임시 페이지)
    path('settings/', views.coming),

    # 👥 친구 기능
    path('friends/', views.friends),             # 친구 목록
    path('add-friend/', views.send_request),     # 친구 요청 보내기
    path('send-request/', views.send_request),   # 친구 요청 (중복 기능)
    path('accept-friend/<int:request_id>/', views.accept_friend),
    path('reject-friend/<int:request_id>/', views.reject_friend),
    path('requests/', views.friend_requests),    # 받은 친구 요청 목록
    path('friend/<int:user_id>/', views.friend_calendar),  # 친구 캘린더 보기

    # 📩 일정 요청 보내기
    path('send-schedule-request/', views.send_schedule_request),

    # 📥 받은 일정 요청 목록
    path('schedule-requests/', views.schedule_requests),

    # ✅ 일정 요청 수락
    path('accept-request/<int:request_id>/', views.accept_request),

    # ❌ 일정 요청 거절
    path('reject-request/<int:request_id>/', views.reject_request),

    # 📤 내가 보낸 요청 목록
    path('sent-requests/', views.sent_requests),

    # 🚫 보낸 요청 취소
    path('cancel-request/<int:request_id>/', views.cancel_request),
]
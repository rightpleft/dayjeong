from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
import json
from .models import ScheduleRequest

from .models import Profile, FriendRequest, Schedule, ScheduleRequest

import calendar
from datetime import date
from collections import defaultdict
from django.shortcuts import render, redirect

# 🔐 로그인
def login_view(request):
    if request.method == 'POST':
        user = authenticate(
            request,
            username=request.POST.get('username'),
            password=request.POST.get('password')
        )

        if user:
            login(request, user)
            return redirect('/')
        else:
            return render(request, 'login.html', {'error': '로그인 실패'})

    return render(request, 'login.html')


# 📝 회원가입
def signup_view(request):
    if request.method == "POST":
        user = User.objects.create_user(
            username=request.POST.get("username"),
            password=request.POST.get("password")
        )
        login(request, user)
        return redirect('/')

    return render(request, "signup.html")


# 🚪 로그아웃
def logout_view(request):
    logout(request)
    return redirect('/login/')


# 🏠 메인
def home(request):
    return render(request, 'home.html')


# 👥 친구 목록
@login_required
def friends(request):
    friends = request.user.profile.friends.all()
    return render(request, 'friends.html', {'friends': friends})


# 📩 친구 요청 보내기
@login_required
def send_request(request):
    if request.method == 'POST':
        to_user = User.objects.get(username=request.POST.get('username'))

        FriendRequest.objects.create(
            from_user=request.user,
            to_user=to_user
        )

    return redirect('/friends/')


# 📥 받은 친구 요청
@login_required
def friend_requests(request):
    requests = FriendRequest.objects.filter(to_user=request.user)
    return render(request, 'requests.html', {'requests': requests})


# ✅ 친구 수락
@login_required
def accept_friend(request, request_id):
    req = FriendRequest.objects.filter(id=request_id).first()

    if not req:
        return redirect('/requests/')

    req.from_user.profile.friends.add(req.to_user)
    req.to_user.profile.friends.add(req.from_user)

    req.delete()

    return redirect('/friends/')


# ❌ 친구 거절
@login_required
def reject_friend(request, request_id):
    req = FriendRequest.objects.filter(id=request_id).first()

    if req:
        req.delete()

    return redirect('/requests/')


# 📩 일정 요청 보내기
@login_required
def send_schedule_request(request):
    data = json.loads(request.body)

    ScheduleRequest.objects.create(
        from_user=request.user,
        to_user_id=data['to_user'],
        date=data['date'],
        title="같이 일정"
    )

    return JsonResponse({'ok': True})


# 📬 받은 일정 요청
@login_required
def schedule_requests(request):
    requests = ScheduleRequest.objects.filter(
        to_user=request.user,
        status='pending'
    )

    return render(request, 'schedule_requests.html', {'requests': requests})


# ✅ 일정 수락
@login_required
def accept_schedule(request, request_id):
    req = ScheduleRequest.objects.filter(id=request_id).first()

    if not req:
        return redirect('/schedule-requests/')

    Schedule.objects.create(user=req.from_user, date=req.date, title=req.title)
    Schedule.objects.create(user=req.to_user, date=req.date, title=req.title)

    req.delete()

    return redirect('/schedule-requests/')


# ❌ 일정 거절
@login_required
def reject_schedule(request, request_id):
    req = ScheduleRequest.objects.filter(id=request_id).first()

    if req:
        req.delete()

    return redirect('/schedule-requests/')

#일정 추가
@login_required
def add_schedule(request):
    # 📌 월 이동 처리
    year = int(request.GET.get('year', date.today().year))
    month = int(request.GET.get('month', date.today().month))

    cal = calendar.monthcalendar(year, month)

    schedules = Schedule.objects.filter(
        user=request.user,
        date__year=year,
        date__month=month
    )

    # 📌 상태 계산
    day_status = {}
    for s in schedules:
        d = s.date.day
        day_status.setdefault(d, []).append(s)

    result = {}
    for d, items in day_status.items():
        if len(items) > 1:
            result[d] = 'red'
        else:
            if items[0].status == 'confirmed':
                result[d] = 'green'
            else:
                result[d] = 'orange'

    # 📌 요청 개수
    request_count = ScheduleRequest.objects.filter(
        to_user=request.user,
        status='pending'
    ).count()

    return render(request, 'add_schedule.html', {
        'calendar': cal,
        'day_status': result,
        'year': year,
        'month': month,
        'request_count': request_count
    })

def coming(request):
    return render(request, 'coming.html')

@login_required
def friend_calendar(request, user_id):
    friend = User.objects.get(id=user_id)

    schedules = Schedule.objects.filter(user=friend)

    return render(request, 'friend_calendar.html', {
        'friend': friend,
        'schedules': schedules
    })

@login_required
def sent_requests(request):
    requests = ScheduleRequest.objects.filter(
        from_user=request.user,
        status='pending'
    )

    return render(request, 'sent_requests.html', {
        'requests': requests
    })

@login_required
def cancel_request(request, request_id):
    req = ScheduleRequest.objects.filter(
        id=request_id,
        from_user=request.user
    ).first()

    if req:
        req.delete()

    return redirect('/sent-requests/')

@login_required
def create_schedule(request):
    if request.method == "POST":
        Schedule.objects.create(
            user=request.user,
            date=request.POST.get("date"),
            title=request.POST.get("title")
        )
        return redirect('/add/')

    return render(request, 'create_schedule.html')
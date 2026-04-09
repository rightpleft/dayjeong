from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User

# 🔐 로그인
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)

            if user.is_staff:
                return redirect('/admin/')
            else:
                return redirect('/')
        else:
            return render(request, 'login.html', {'error': '로그인 실패'})

    return render(request, 'login.html')

# 📝 회원가입
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login

def signup_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        password2 = request.POST.get("password2")

        # ✅ 1. username 체크
        if not username:
            return render(request, "signup.html", {
                "error": "아이디를 입력해주세요"
            })

        # ✅ 2. 비밀번호 확인
        if password != password2:
            return render(request, "signup.html", {
                "error": "비밀번호가 다릅니다"
            })

        # ✅ 3. 중복 체크
        if User.objects.filter(username=username).exists():
            return render(request, "signup.html", {
                "error": "이미 존재하는 아이디입니다"
            })

        # ✅ 4. 유저 생성
        user = User.objects.create_user(
            username=username,
            password=password
        )

        # ✅ 5. 자동 로그인 🔥
        login(request, user)

        # ✅ 6. 홈 이동
        return redirect('/')

    return render(request, "signup.html")

# 🚪 로그아웃
def logout_view(request):
    logout(request)
    return redirect('/login/')

# 🏠 메인페이지
def home(request):
    return render(request, 'home.html')

# ➕ 일정 추가
import calendar
from datetime import date

def add_schedule(request):
    today = date.today()
    year = today.year
    month = today.month

    # 🔥 달력 생성
    cal = calendar.monthcalendar(year, month)

    # 🔥 일정 저장 처리
    if request.method == 'POST':
        title = request.POST.get('title')
        selected_date = request.POST.get('date')

        print("날짜:", selected_date)
        print("일정:", title)

        return redirect('/')

    return render(request, 'add_schedule.html', {
        'username': request.user.username,
        'calendar': cal,
        'year': year,
        'month': month,
    })

from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import Friend
from django.http import JsonResponse
import json

from .models import Friend, Schedule, ScheduleRequest

# 친구 목록
@login_required
def friend_calendar(request, user_id):
    friend = User.objects.get(id=user_id)

    schedules = Schedule.objects.filter(user=friend)

    return render(request, 'friend_calendar.html', {
        'friend': friend,
        'schedules': schedules
    })

# 친구 요청 보내기
@login_required
def send_request(request):
    username = request.POST.get("username")

    try:
        to_user = User.objects.get(username=username)

        if to_user != request.user:
            Friend.objects.get_or_create(
                from_user=request.user,
                to_user=to_user,
                status='pending'
            )
    except:
        pass

    return redirect('/friends/')

# 받은 요청 목록
@login_required
def friend_requests(request):
    requests = Friend.objects.filter(
        to_user=request.user,
        status='pending'
    )
    return render(request, 'friend_requests.html', {'requests': requests})

# 요청 수락
@login_required
def accept_request(request, id):
    f = Friend.objects.get(id=id, to_user=request.user)

    f.status = 'accepted'
    f.save()

    # 양방향 친구 생성
    Friend.objects.get_or_create(
        from_user=request.user,
        to_user=f.from_user,
        status='accepted'
    )

    return redirect('/friends/')

# 요청 거절
@login_required
def reject_request(request, id):
    Friend.objects.filter(id=id, to_user=request.user).delete()
    return redirect('/friends/')

# 일정 추가 (DB 저장)
def add_schedule(request):
    if request.method == "POST":
        title = request.POST.get("title")
        status = request.POST.get("status")
        date_str = request.POST.get("date")

        Schedule.objects.create(
            user=request.user,
            title=title,
            status=status,
            date=date_str
        )

        return redirect('/')

    return render(request, 'add_schedule.html')

# 👀 친구 캘린더 보기
@login_required
def friend_calendar(request, user_id):
    friend = User.objects.get(id=user_id)

    schedules = Schedule.objects.filter(user=friend)

    return render(request, 'friend_calendar.html', {
        'friend': friend,
        'schedules': schedules
    })


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
def accept_schedule(request, id):
    r = ScheduleRequest.objects.get(id=id)

    r.status = 'accepted'
    r.save()

    # 🔥 핵심: 둘 다 일정 생성
    Schedule.objects.create(
        user=r.from_user,
        date=r.date,
        title=r.title
    )

    Schedule.objects.create(
        user=r.to_user,
        date=r.date,
        title=r.title
    )

    return redirect('/schedule-requests/')


# ❌ 일정 거절
@login_required
def reject_schedule(request, id):
    ScheduleRequest.objects.filter(id=id).update(status='rejected')
    return redirect('/schedule-requests/')

@login_required
def friends(request):
    friends = Friend.objects.filter(
        from_user=request.user,
        status='accepted'
    )
    return render(request, 'friends.html', {'friends': friends})

def coming(request):
    return render(request, 'coming.html')
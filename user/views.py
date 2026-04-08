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
from .models import Friend, Schedule
from datetime import date

# 친구 목록
def friends(request):
    friends = Friend.objects.filter(user=request.user, blocked=False)
    return render(request, 'friends.html', {'friends': friends})

# 친구 추가
def add_friend(request):
    username = request.POST.get("username")

    try:
        friend_user = User.objects.get(username=username)

        if friend_user != request.user:
            Friend.objects.get_or_create(
                user=request.user,
                friend=friend_user
            )
    except:
        pass

    return redirect('/friends/')

# 친구 삭제
def delete_friend(request, id):
    Friend.objects.filter(id=id, user=request.user).delete()
    return redirect('/friends/')

# 친구 차단
def block_friend(request, id):
    f = Friend.objects.get(id=id, user=request.user)
    f.blocked = True
    f.save()
    return redirect('/friends/')

# 친구 캘린더 보기
def friend_calendar(request, user_id):
    friend = User.objects.get(id=user_id)
    schedules = Schedule.objects.filter(user=friend)

    return render(request, 'friend_calendar.html', {
        'friend': friend,
        'schedules': schedules
    })

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

def coming(request):
    return render(request, 'coming.html')
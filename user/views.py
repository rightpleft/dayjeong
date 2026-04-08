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

def coming(request):
    return render(request, 'coming.html')
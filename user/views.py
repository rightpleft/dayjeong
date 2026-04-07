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
def signup_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        if User.objects.filter(username=username).exists():
            return render(request, 'signup.html', {
                'error': '이미 존재하는 아이디입니다'
            })

        user = User.objects.create_user(username=username, password=password)
        login(request, user)

        return redirect('/')

    return render(request, 'signup.html')

# 🚪 로그아웃
def logout_view(request):
    logout(request)
    return redirect('/login/')

# 🏠 메인페이지
def home(request):
    return render(request, 'home.html')

# ➕ 일정 추가
def add_schedule(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        print("일정:", title)
        return redirect('/')

    return render(request, 'add_schedule.html')
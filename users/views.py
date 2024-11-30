from django.contrib import auth
from django.contrib.auth.models import User
from django.shortcuts import redirect, render


# 회원가입
def signup(request):
    if request.method == "POST":
        if request.POST["password1"] == request.POST["password2"]:
            user = User.objects.create_user(username=request.POST["username"], password=request.POST["password1"])
            auth.login(request, user)
            return redirect("home")
    return render(request, "signup.html")


# 로그인 기능
def login(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        # 입력 내용이 DB에 있는지 확인
        user = auth.authenticate(request, username=username, password=password)

        if user is not None:  # is not None = None이 아니라면 = 회원이라면
            auth.login(request, user)
            return redirect("home")
        else:
            return render(request, "login.html", {"error": "username or password is incorrect"})
    else:
        return render(request, "login.html")


# 로그아웃 기능
def logout(request):
    if request.method == "POST":
        auth.logout(request)
        return redirect("home")
    return render(request, "login.html")

from django.shortcuts import render
from django.http import HttpResponse


def home(request):
    return render(request, "index.html")


def login(request):
    if request.POST:

        login_data = request.POST.dict()

        print("LOGIN")
        email = login_data.get("email")
        password = login_data.get("password")
        print(email, password)

    return render(request, "login.html")


def signup(request):
    if request.POST:

        signup_data = request.POST.dict()

        print("SIGNUP")
        name = signup_data.get("name")
        email = signup_data.get("email")
        password = signup_data.get("password")
        repeat_pwd = signup_data.get("repeatpassword")
        print(name, email, password, repeat_pwd)

    return render(request, "signup.html")

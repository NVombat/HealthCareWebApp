from django.shortcuts import render, redirect

from .errors import (
    InvalidUserCredentialsError,
    UserAlreadyExistsError,
    UserDoesNotExistError,
)
from . import s, User


def home(request):
    return render(request, "index.html")


def signup(request):
    if request.POST:

        signup_data = request.POST.dict()

        print("SIGNUP")
        name = signup_data.get("name")
        email = signup_data.get("email")
        password = signup_data.get("password")
        repeat_password = signup_data.get("repeatpassword")
        print(name, email, password, repeat_password)

        if password == repeat_password:
            print("Password Match")
            try:
                User.insert_user(name, email, password)
                print("Data Inserted Successfully")
                s.error = "Sign Up Successful"
                return redirect("/login")

            except UserAlreadyExistsError as e:
                return render(request, "login.html", {"error": str(e)})

        else:
            print("Password & Repeat Password DO NOT Match")
            return render(
                request,
                "signup.html",
                {"error": "Password & Repeat Password DO NOT Match"},
            )

    return render(request, "signup.html")


def login(request):
    if request.POST:

        login_data = request.POST.dict()

        print("LOGIN")
        email = login_data.get("email")
        password = login_data.get("password")
        print(email, password)

        try:
            if User.check_hash(email, password):
                print("Login Successful")
                s.email = email
                return redirect("/booking")

        except InvalidUserCredentialsError as e:
            return render(request, "login.html", {"error": str(e)})

        except UserDoesNotExistError as e:
            return render(request, "login.html", {"error": str(e)})

    else:
        if hasattr(s, "error"):
            return render(request, "login.html", {"error": s.error})
        return render(request, "login.html")


def booking(request):
    if request.POST:

        booking_data = request.POST.dict()

        print("BOOKING")
        name = booking_data.get("name")
        desc = booking_data.get("desc")
        date = booking_data.get("date")
        doc = booking_data.get("doctors")

        print(name, desc, date, doc)

        return render(request, "index.html")

    else:
        if hasattr(s, "email"):
            return render(request, "booking.html", {"email": s.email})
        return render(request, "booking.html")

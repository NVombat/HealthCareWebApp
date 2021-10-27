from django.shortcuts import render, redirect

from .errors import (
    AppointmentAlreadyExistsError,
    DoctorUnavailableError,
    InvalidUserCredentialsError,
    NoAppointmentsError,
    UserAlreadyExistsError,
    UserDoesNotExistError,
)
from . import s, User, Appointment


def home(request):
    if hasattr(s, "name"):
        try:
            apts = Appointment.fetch_appointments(s.name)
            print(apts)
            return render(request, "appointments.html", {"data" : apts})

        except NoAppointmentsError as npe:
            return render(request, "index.html", {"error": str(npe)})

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

        try:
            Appointment.insert_appointment(name, desc, date, doc)

        except AppointmentAlreadyExistsError as aae:
            return render(request, "booking.html", {"error": str(aae)})

        except DoctorUnavailableError as due:
            return render(request, "booking.html", {"error": str(due)})

        s.name = name
        return redirect("/")

    else:
        if hasattr(s, "email"):
            return render(request, "booking.html", {"email": s.email})
        return render(request, "booking.html")

from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from account.models import CustomUser
from .forms import SignUpForm
from .forms import LoginForm
# Create your views here.


def login(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]
            user = authenticate(request, username=email, password=password)
            if user is not None:
                auth_login(request, user)
                return redirect("home/index")
        else:
            print("Form errors:", form.errors)
            print("Non-field errors:", form.non_field_errors())
    context = {"form": LoginForm}
    return render(request, "account/login.html", context)


def signup(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect("home/index")
        else:
            print("Form errors:", form.errors)
            print("Non-field errors:", form.non_field_errors())

    context = {"form": SignUpForm}
    return render(request, "account/signup.html", context)


def edit(request):
    if not request.user.is_authenticated:
        return redirect("account/login")

    user = request.user
    custom_user = CustomUser.objects.get(email=user)
    print(custom_user)
    context = {"user": custom_user}
    return render(request, "account/edit.html", context)


def dashboard(request):
    user = request.user
    if user.is_authenticated:
        context = {
            "first_name": user.first_name,
            "last_name": user.last_name,
            "email": user.email,
            "password": user.password,
            "phone": user.phone,
            "city": user.city,
            "address": user.address,
        }
        return render(request, "account/dashboard.html", context)
    return redirect("account/login")


def logout(request):
    auth_logout(request)
    return redirect("home/index")

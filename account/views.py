from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import check_password
from account.models import CustomUser
from order.models import Order, OrderDetail
from wishlist.models import Wishlist
from .forms import SignUpForm, LoginForm, ForgotPasswordForm, ResetPasswordForm
from django.core.mail import send_mail
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from .tokens import account_activation_token
from django.utils.encoding import force_str
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
# Create your views here.


def login(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]
            print(email, password)
            user = authenticate(request, email=email, password=password)
            print(user)
            if user is not None:
                auth_login(request, user)
                return redirect("home/index")
        else:
            print("Form errors:", form.errors)
            print("Non-field errors:", form.non_field_errors())
    context = {"form": LoginForm}
    return render(request, "account/login.html", context)

    
def register(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            password = form.cleaned_data["password"]
            print(password)
            user.is_active = False
            user.save()

            current_site = get_current_site(request)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = account_activation_token.make_token(user)

            activation_link = reverse('activate', kwargs={'uidb64': uid, 'token': token})
            activation_url = f"http://{current_site.domain}{activation_link}"
            print(activation_url)
            send_mail(
                subject='Activate your account',
                message=f'Click the link to activate your account: {activation_url}',
                from_email='noreply@yourdomain.com',
                recipient_list=[user.email],
            )
            return redirect('account/login')
        else:
            print(form.errors)
            
    context = {"form": SignUpForm}
    return render(request, "account/signup.html", context)
        
    
def forget_password_view(request):
    if request.method == "POST":
        form = ForgotPasswordForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
            user = CustomUser.objects.get(email=email)
            if user and user.is_active:
                uid = urlsafe_base64_encode(force_bytes(user.pk))
                token = default_token_generator.make_token(user)
                reset_url = request.build_absolute_uri(
                    reverse("renew_password", kwargs={"uidb64": uid, "token": token})
                )
                print(reset_url)
                send_mail(
                    subject='Renew your password',
                    message=f'Click the link to renew your password: {reset_url}',
                    from_email='noreply@yourdomain.com',
                    recipient_list=[user.email],
                )
    context = {
        "form": ForgotPasswordForm()
    }
    return render(request, "account/forgot_password.html", context)


def renew_password(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = CustomUser.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        if request.method == "POST":
            form = ResetPasswordForm(request.POST)
            if form.is_valid():
                new_password = form.cleaned_data["new_password"]
                user.set_password(new_password)
                user.save()
                messages.success(request, "Password has been reset. You can now log in.")
                return redirect("account/login")
        else:
            form = ResetPasswordForm()
        return render(request, "account/renew_password.html", {"form": form})
    else:
        messages.error(request, "The reset link is invalid or has expired.")
        return redirect("account/forgot_password")

def activate_account(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = CustomUser.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
        user = None

    if user and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        return render(request, 'account/activation_success.html')
    else:
        return render(request, 'account/activation_invalid.html')

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

@login_required
def edit(request):
    if not request.user.is_authenticated:
        return redirect("account/login")

    user = request.user
    custom_user = CustomUser.objects.get(email=user)
    print(custom_user)
    context = {"user": custom_user}
    return render(request, "account/edit.html", context)

@login_required
def dashboard(request):
    user = request.user
    if user.is_authenticated:
        context = {
            "first_name": user.first_name,
            "last_name": user.last_name,
            "email": user.email,
            "password": user.password,
            "hidden_password": "*" * len(user.password),
            "phone": user.phone,
            "city": user.city,
            "address": user.address,
        }
        return render(request, "account/dashboard.html", context)
    return redirect("account/login")

@login_required
def order_history(request):
    user = request.user
    if user.is_authenticated:
        orders = Order.objects.filter(user=user).order_by("-created_at")
        context = {"orders": orders, "total_orders": len(orders)}
        return render(request, "account/order-history.html", context)
    return redirect("account/login")

@login_required
def address_book(request):
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
        return render(request, "account/address-book.html", context)
    return redirect("account/login")

@login_required
def wishlist(request):
    user = request.user
    if user.is_authenticated:
        context = {
            "wishlist": Wishlist.objects.filter(user=user)
        }
        return render(request, "account/wishlist.html", context)
    return redirect("account/login")


@login_required
def payment(request):
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
        return render(request, "account/payment.html", context)
    return redirect("account/login")


@login_required
def logout(request):
    auth_logout(request)
    return redirect("home/index")

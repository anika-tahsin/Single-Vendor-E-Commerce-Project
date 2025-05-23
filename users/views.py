from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, get_user_model, logout
from django.contrib.auth.decorators import login_required
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator

from .forms import customUserRegistrationForm
from .models import customerUser
from users.utils import verification_email_send, password_reset_email

User = get_user_model()

# User Signup
def user_signup(request):
    if request.method == "POST":
        form = customUserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = True  # Prevent login before verification if False
            user.save()
            verification_email_send(request, user)  # Send verification email
            messages.info(request, "A verification email has been sent to your inbox.")
            return redirect("login")
        else:
            print(form.errors)
            messages.error(request, "Something went wrong.")
            return render(request, "users/register.html", {"form": form})
    
    form = customUserRegistrationForm()

    return render(request, "users/register.html", {"form": form})

# Email Verification
def verify_email(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = customerUser.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, customerUser.DoesNotExist):
        user = None

    if user and default_token_generator.check_token(user, token):
        user.is_verified = True
        user.is_active = True
        user.save()
        messages.success(request, "Your email has been verified successfully.")
        return redirect("login")
    else:
        messages.error(request, "The verification link is invalid or has expired.")
        return redirect("user_signup")

#  User Login
def user_login(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        print(f"Trying login with email: {email} and password: {password}")

        user = authenticate(request, email=email, password=password)  # key change here

        print(f"Authenticated user: {user}")

        if not user:
            messages.error(request, "Invalid email or password")
            return render(request, "users/login.html")

        elif not user.is_verified:
            messages.error(request, "Email is not verified yet")
            return redirect("verify_email")

        else:
            login(request, user)
            messages.success(request, f"Welcome back, {user.fullname}")
            return redirect("account")

    return render(request, "users/login.html")


#  Logout
@login_required
def user_logout(request):
    logout(request)
    return redirect("login")

#  Request Password Reset
def reset_password(request):
    if request.method == "POST":
        email = request.POST.get("email")
        try:
            user = customerUser.objects.get(email=email)
            password_reset_email(request, user)
            messages.success(request, "Check your email to reset your password.")
        except customerUser.DoesNotExist:
            messages.error(request, "No user found with this email.")
    return render(request, "users/forgot.html")

#  Confirm Reset Token
def confirm_password_reset(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = customerUser.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, customerUser.DoesNotExist):
        user = None

    if user and default_token_generator.check_token(user, token):
        login(request, user)
        return redirect("change_password")
    else:
        messages.error(request, "Reset link is invalid or expired.")
        return redirect("login")

#  Change Password
@login_required
def change_password(request):
    if request.method == "POST":
        password = request.POST.get("password")
        user = request.user
        user.set_password(password)
        user.save()
        messages.success(request, "Password changed successfully. Please login again.")
        logout(request)
        return redirect("login")
    return render(request, "users/new_password.html")

#  User Account View
@login_required
def user_account(request):
    user = request.user
    if request.method == "POST":
        user.fullname = request.POST.get("fullname", user.fullname)
        user.email = request.POST.get("email", user.email)
        user.mobile = request.POST.get("mobile", user.mobile)
        user.address = request.POST.get("address", user.address)
        user.city = request.POST.get("city", user.city)
        user.country = request.POST.get("country", user.country)
        user.save()
        messages.success(request, "Profile updated successfully.")

    return render(request, "users/user_account.html", {'user_info': user})

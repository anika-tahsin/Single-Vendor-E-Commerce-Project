import email
from django.shortcuts import render, redirect
from django.contrib import messages

from django.contrib.auth import authenticate, login, get_user_model, logout
from django.contrib.auth.decorators import login_required

from .forms import customUserRegistrationForm
from .models import customerUser

from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator

from users.utils import verification_email_send, password_reset_email

# Create your views here.

User = get_user_model()

# User Signup/ Registration view
def user_signup(request):
    if request.method == "POST":
        form = customUserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.info(request, "A verification mail has been sent to your email")
            return redirect("login")
        else:
            print(form.errors)
            return render(request, "users/register.html", context={"form": form})
 
    form = customUserRegistrationForm()
    return render(request, "users/register.html", context={"form": form})


# Email Verification 

def verify_email(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = customerUser.objects.get(pk=uid)

    except(TypeError, ValueError, OverflowError, customerUser.DoesNotExist):
        user = None

    if user and default_token_generator.check_token(user, token):
        user.is_verified = True
        user.save()

        messages.success(request, "Your email has been verified successfully")
        return redirect("login")
    
    else:
        messages.error(request, "The verification link is either invalid or expired.")
        return redirect("signup")



# User Login view
def user_login(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        user = authenticate(request, email=email, password=password)

        if not user:
            messages.error(request, "Invalid username or password")

        elif not user.is_verified:
            messages.error(request, "Email is not verified yet")

        else:
            login(request,user)
            messages.success(request, f"Welcome back, {user.username}")
            #return redirect('login')
            return redirect("account")
            

    return render(request, "users/login.html")


@login_required
def user_logout(request):
    logout(request)
    return redirect("signup")
    #return redirect("home")


# Reset password
def reset_password(request):
    if request.method == "POST":
        email = request.POST.get("email")

    try:
        user = customerUser.objects.get(email=email)
    except customerUser.DoesNotExist:
        messages.error(request, "No such user exists")
        return redirect("password-reset")
    
    #return render(request, "users/forgot.html")


# Password reset email

def confirm_password_reset(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = customerUser.objects.get(pk=uid)

    except(TypeError, ValueError, OverflowError, customerUser.DoesNotExist):
        user = None

    if user and default_token_generator.check_token(user, token):
        user.is_verified = True
        user.save()
        login(request, user)
        return redirect("change-password")
    
    else:
        messages.error(request, "The verification link is either invalid or expired.")
        return redirect("login")
    


# Change or get new password
@login_required
def change_password(request):
   if request.method == "POST":
       password = request.POST.get("password")
       user = request.user
       user.set_password(password)
       user.save()

       messages.success(request, "Successfully changed password")
       return redirect("account")
    #return render(request, "users/new_password.html")


# User account view

@login_required
def user_account(request):
    user = request.user
    
    if request.method == "POST":
        
        user.fullname =  request.POST.get("fullname", user.fullname)
        user.email = request.POST.get("email", user.email)
        user.mobile = request.POST.get("mobile", user.mobile)
        user.address = request.POST.get("address", user.address)
        user.city = request.POST.get("city", user.city)
        user.country = request.POST.get("country", user.country)
        user.save()

    return render(request, "users/user_account.html", {'user_info': user})
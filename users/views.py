from django.shortcuts import render, redirect
from django.contrib import messages

from django.contrib.auth import authenticate, login, get_user_model, logout
from django.contrib.auth.decorators import login_required

from .forms import customUserRegistrationForm

# Create your views here.

User = get_user_model()

# User Signup/ Registration view
def user_signup(request):
    if request.method == "POST":
        form = customUserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.info(request, "We have sent a verification mail")
            return redirect("signup")
        else:
            print(form.errors)
            return render(request, "users/register.html", context={"form": form})
 
    form = customUserRegistrationForm()
    return render(request, "users/register.html", context={"form": form})


# User Login view
def user_login(request):
    if request.method == "POST":
        user_input = request.POST.get("username")
        password = request.POST.get("password")

        try:
            user_obj= User.objects.get(email=user_input)
            username = user.obj.username
        except User.DoesNotExist:
            username = user_input

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request,user)
            messages.success(request, f"Welcome back, {user.username}")
            return redirect('login')
            #return redirect('home')
        elif not user.is_verified:
            messages.error(request, "Email is not verified")
        else:
            messages.error(request, "Invalid username or password")

    return render(request, "users/login.html")


@login_required
def user_logout(request):
    logout(request)
    return redirect("signup")
    #return redirect("home")

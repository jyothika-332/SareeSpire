from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib import messages,auth
from adminlogin.views import dashboard
from django.views.decorators.cache import cache_control
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate,login
from django.http import HttpResponse


# Create your views here.

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def loginpage(request):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            return redirect('dashboard')
        else:
            return redirect('home')
    if request.method=='POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        if username.strip() == '' or password.strip() =='':
            messages.error(request,"Field can't be blank!!!")
            return redirect('login') 

        user = authenticate(username = username,password = password)
        if user is not None :
            login(request,user)
            if request.user.is_superuser:
                return redirect('dashboard')            
            else:
               return redirect('home') 
        else:
            messages.error(request,"Username or Password Incorrect!!")
            return redirect('login')

    return render(request,'accounts/login.html')

# @cache_control(no_cache=True, must_revalidate=True, no_store=True)
def signuppage(request):
    if request.method=='POST':
         firstname = request.POST.get('firstname')
         lastname = request.POST.get('lastname')
         username = request.POST.get('username')
         email = request.POST.get('email')
         password1 = request.POST.get('password1')
         password2 = request.POST.get('password2')

         if password1==password2:
            user = User.objects.create_user(first_name=firstname,last_name=lastname,username=username,email=email,password=password1)
            print('user created successfuly')
            return redirect('login')

    return render(request,'accounts/signup.html')

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='login')
def signout(request):
    auth.logout(request)
    return redirect('login')



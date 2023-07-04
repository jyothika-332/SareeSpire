from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib import messages,auth
from adminlogin.views import dashboard
from django.views.decorators.cache import cache_control
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate,login
from django.http import HttpResponse
from userprofile.models import User_Otp
from django.contrib import auth
from django.core.mail import send_mail
from django.conf import settings
import random
from django.core.exceptions import ValidationError




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


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def signuppage(request):
    if request.method=='POST':
        get_otp=request.POST.get('otp')
        if get_otp:
            get_email=request.POST.get('email')
            usr=User.objects.get(email=get_email)
            if int(get_otp)==User_Otp.objects.filter(user=usr).last().otp:
                usr.is_active=True
                usr.save()
                auth.login(request,usr)
                messages.success(request,f'Account is created for {usr.email}')
                User_Otp.objects.filter(user=usr).delete()
                return redirect('userprofile')
            else:
                messages.warning(request,f'You Entered a Wrong OTP')
                return render(request,'accounts/signup.html',{'otp':True,'usr':usr})

        else:


            firstname = request.POST.get('firstname')
            lastname = request.POST.get('lastname')
            username = request.POST.get('username')
            email = request.POST.get('email')
            password1 = request.POST.get('password1')
            password2 = request.POST.get('password2')

            if username.strip() == '' or firstname.strip() =='' or email.strip() =='':
                messages.error(request,"Field can't be blank!!!")
                return redirect('signup')
        
            if password1==password2:
                eml = User.objects.filter(email=email)
                if eml:
                    messages.success(request,'Email Already Exist')
                    return render(request,'accounts/signup.html') 
                try:
                    usr = User.objects.get(email=email)
                except:
                    usr = User.objects.create_user(first_name=firstname,last_name=lastname,username=username,email=email,password=password1)
                    usr.is_active = False
                    usr.save()

                    user_otp=random.randint(100000,999999)
                    User_Otp.objects.create(user=usr,otp=user_otp)
                    mess=f'Hello\t{usr.username},\nYour OTP to verify your account for SareeSpire is {user_otp}\nThanks!'
                    send_mail(
                            "welcome to SareeSpire Verify your Email",
                            mess,
                            settings.EMAIL_HOST_USER,
                            [usr.email],
                            fail_silently=False
                        )
                    return render(request,'accounts/signup.html',{'otp':True,'usr':usr})

    return render(request,'accounts/signup.html')



@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='login')
def signout(request):
    auth.logout(request)
    return redirect('home')


def forgotpassword(request):
    if request.method=='POST':
        get_otp=request.POST.get('otp')
        if get_otp:
            get_email=request.POST.get('email')
            usr=User.objects.get(email=get_email)
            if int(get_otp)==User_Otp.objects.filter(user=usr).last().otp:
                user = User.objects.get(email = get_email)
                password1 = request.POST.get('password1')
                password2 = request.POST.get('password2')
                Pass = ValidatePassword(password1)
                if password1 == password2:
                    if Pass is False:
                        context ={
                                'pre_otp':get_otp,
                            }
                        messages.info(request,'Enter Strong Password')
                        return render(request,'accounts/forgotpassword.html',context)
                    user.set_password(password1)
                    user.save()
                    User_Otp.objects.filter(user=usr).delete()
                    return redirect('login')
                else:
                    messages.error(request,"Password dosn't match")
            else:
                messages.warning(request,f'You Entered a wrong OTP')
                return render(request,'accounts/forgotpassword.html',{'otp':True,'usr':usr})
            
        # User rigistration validation
        else:
            email = request.POST['email']
            # null values checking
            check = [email]
            for values in check:
                if values == '':
                    context ={
                       'pre_email':email,
                    }
                    return render(request,'accounts/forgotpassword.html',context)
                else:
                    pass

            result = validateEmail(email)
            if result is False:
                context ={
                        'pre_email':email,
                    }
                messages.info(request,'Enter valid email')
                return render(request,'accounts/forgotpassword.html',context)
            else:
                pass
            
            if User.objects.filter(email = email).exists():
                usr = User.objects.get(email=email) 
                user_otp=random.randint(100000,999999)
                User_Otp.objects.create(user=usr,otp=user_otp)
                mess=f'Hello\t{usr.username},\nYour OTP to verify your account for SareeSpire is {user_otp}\nThanks!'
                send_mail(
                        "welcome to SareeSpire Verify your Email",
                        mess,
                        settings.EMAIL_HOST_USER,
                        [usr.email],
                        fail_silently=False
                    )
                return render(request,'accounts/forgotpassword.html',{'otp':True,'usr':usr})
            else:
                messages.info(request,'You have not an account')
                return render (request, 'accounts/forgotpassword.html')
    return render (request, 'accounts/forgotpassword.html')


def ValidatePassword(password):
    from django.contrib.auth.password_validation import validate_password
    try:
        validate_password(password)
        return True
    except ValidationError:
        return False

 
def validateEmail(email):
    from django.core.validators import validate_email
    try:
        validate_email(email)
        return True
    except ValidationError:
        return False
        
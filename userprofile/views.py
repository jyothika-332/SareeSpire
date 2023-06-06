from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.views.decorators.cache import cache_control
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from userprofile.models import UserAddress
from django.contrib.auth.hashers import check_password
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.models import User


# Create your views here.
def userprofile(request):
    address = UserAddress.objects.filter(customer_id=request.user)
    addresses = {
        'addresses': address
    }

    return render(request,'userprofile/userprofile.html',addresses)

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='login')
def add_address(request):
    if request.method == 'POST':
        house_name = request.POST['house_name']
        city = request.POST['city']
        state = request.POST['state']
        country = request.POST['country']
        pincode = request.POST['pincode']
        # try:
        #     is_super = request.POST['is_superuser']
        # except: 
        #     is_super = False

        if house_name.strip() == '' or city.strip() == '' or state.strip() == '' or country.strip() == '' or pincode.strip() == '':
            messages.error(request, "Fields can't be blank")
            return redirect('addaddress')   
        if UserAddress.objects.filter(housename=house_name).exists():
            messages.error(request, 'Address already exists')
            return redirect('addaddress')
        address = UserAddress(customer_id=request.user,housename=house_name,city=city,state=state,country=country,pincode=pincode)  
        address.save()
        messages.success(request, 'Address Added successfully')
        return redirect('userprofile')
    return render(request,'userprofile/addaddress.html')


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='login')
def changepassword(request):
    if request.method == 'POST':
        old_password = request.POST.get('old_password')
        new_password = request.POST.get('new_password')
        confirm_new_password = request.POST.get('confirm_new_password')
#  Validation
        if new_password != confirm_new_password:
            messages.error(request,'Password did not match')
            return redirect('userprofile')
        user = User.objects.get(username = request.user)
        if check_password(old_password, user.password):
            user.set_password(new_password)
            user.save()

            update_session_auth_hash(request, user)

            messages.success(request, 'Password updated successfully')
            return redirect('userprofile')
        else:
            messages.error(request, 'Invalid old password')
            return redirect('userprofile')
    return render(request,'userprofile/userprofile.html')

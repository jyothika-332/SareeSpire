from django.shortcuts import render,redirect
from home.models import Ads
from product.models import Product, Categories
from django.views.decorators.cache import cache_control
from django.contrib.auth.decorators import login_required
from django.contrib import messages

# Create your views here.

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def homepage(request):
    ads = {
        'ads' : Ads.objects.all(),
        'catergory': Categories.objects.all(),
    }
    return render(request,'homepage/homepage.html',ads)



@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='login')
def admin_ads(request):
    context ={
        'ads': Ads.objects.all(),
    }
    return render(request,'homepage/admin_ads.html',context)



@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='login')
def add_ads(request):
    if request.method == 'POST':
        ads = request.POST['ads']
        image = request.FILES.get('image')
        try:
            is_super = request.POST['is_superuser']
        except: 
            is_super = False

        if ads.strip() == '' or image == '':
            messages.error(request, "Fields can't be blank")
            return redirect('add_ads')   
        if Ads.objects.filter(ad_name=ads).exists():
            messages.error(request, 'Ad already exists')
            return redirect('add_ads')
        ads = Ads(ad_name=ads,image=image)  
        ads.save()
        messages.success(request, 'Ads Added successfully')
        return redirect('admin_ads')
    return render(request,'homepage/add_ads.html')



@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='login')
def edit_ads(request,ads_id):
    if request.method =='POST':
        ads = request.POST['ads']
        image = request.FILES.get('image')
        if ads == '' or image == '':
            messages.error(request, "Fields can't be blank")
            return redirect('edit_ads', ads_id)

        ads = Ads.objects.get(id=ads_id)
        ads.ad_name = ads
        if image:
            ads.image = image

        messages.success(request, 'Ads updated successfully')
        ads.save()
        return redirect('admin_ads')
    ads = Ads.objects.get(id=ads_id)
    
    return render(request, 'homepage/edit_ads.html',{'ads': ads})


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='login')
def delete_ads(request,ads_id):
    ads = Ads.objects.get(id=ads_id)
    ads.delete()
    messages.success(request,'Ads Deleted successfully')
    return redirect('admin_ads')
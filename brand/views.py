from django.shortcuts import render,redirect
from django.views.decorators.cache import cache_control
from django.contrib.auth.decorators import login_required
from product.models import Brand
from django.contrib import messages
# Create your views here.

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='login')
def adminbrand(request):
    dictionary={
        'brnd': Brand.objects.all()
    }
    return render(request,'brand/adminbrand.html',dictionary)

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='login')
def addbrand(request):
    if request.method == 'POST':
        brand_name = request.POST['brand_name']
        description = request.POST['description']
        image = request.FILES.get('image')
        try:
            is_super = request.POST['is_superuser']
        except: 
            is_super = False

        if brand_name.strip() == '' or description.strip() == '':
            messages.error(request, "Fields can't be blank")
            return redirect('addbrand')   
        if Brand.objects.filter(brand_name=brand_name).exists():
            messages.error(request, 'Brand already exists')
            return redirect('addbrand')
        brnd = Brand(brand_name=brand_name,description=description,image=image)  
        brnd.save()
        messages.success(request, 'Brand Added successfully')
        return redirect('adminbrand')
    return render(request,'brand/addbrand.html') 

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='login')
def editbrand(request,brnd_id):
    if request.method =='POST':
        brand_name = request.POST['brand_name']
        description = request.POST['description']
        image = request.FILES.get('image')
        if brand_name == '' or description == '':
            messages.error(request, "Fields can't be blank")
            return redirect('editbrand', brnd_id)
        
        brnd = Brand.objects.get(id=brnd_id)
        brnd.brand_name = brand_name
        brnd.description = description
        if image:
            brnd.image = image
        messages.success(request, 'Brand updated successfully')
        brnd.save()
        return redirect('adminbrand')
    brnd = Brand.objects.get(id=brnd_id)
    return render(request, 'brand/editbrand.html',{'brnd': brnd})

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='login')
def deletebrand(request,brnd_id):
    brnd = Brand.objects.get(id=brnd_id)
    brnd.delete()
    messages.success(request,'Brand Deleted successfully')
    return redirect('adminbrand')
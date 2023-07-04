from django.shortcuts import render,redirect
from django.views.decorators.cache import cache_control
from django.contrib.auth.decorators import login_required
from product.models import Categories
from django.contrib import messages
# Create your views here.


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='login')
def admincategory(request):
    context={
        'cat': Categories.objects.all()
    }
    return render(request,'category/admincategory.html',context)


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='login')
def addcategory(request):
    if request.method == 'POST':
        category_name = request.POST['category_name']
        description = request.POST['description']
        image = request.FILES.get('image')
        try:
            is_super = request.POST['is_superuser']
        except: 
            is_super = False

        if category_name.strip() == '' or description.strip() == '' or image == '':
            messages.error(request, "Fields can't be blank")
            return redirect('addcategory')   
        if Categories.objects.filter(product_name=category_name).exists():
            messages.error(request, 'Category already exists')
            return redirect('addcategory')
        cat = Categories(product_name=category_name,description=description,image=image)  
        cat.save()
        messages.success(request, 'Category Added successfully')
        return redirect('admincategory')
    return render(request,'category/addcategory.html') 


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='login')
def deletecategory(request,cat_id):
    prod = Categories.objects.get(id=cat_id)
    prod.delete()
    messages.success(request,'Category Deleted successfully')
    return redirect('admincategory')



@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='login')
def editcategory(request,cat_id):
    if request.method =='POST':
        category_name = request.POST['category_name']
        description = request.POST['description']
        image = request.FILES.get('image')
        if category_name == '' or description == '':
            messages.error(request, "Fields can't be blank")
            return redirect('editcategory', cat_id)
        
        cat = Categories.objects.get(id=cat_id)
        cat.product_name = category_name
        cat.description = description
        if image:
            cat.image = image
        messages.success(request, 'category updated successfully')
        cat.save()
        return redirect('admincategory')
    cat = Categories.objects.get(id=cat_id)
    return render(request, 'category/editcategory.html',{'cat': cat})

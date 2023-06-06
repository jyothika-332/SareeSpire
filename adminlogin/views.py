from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.views.decorators.cache import cache_control
from django.contrib.auth.decorators import login_required
from product.models import Product,Categories,Brand

# Create your views here.

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='login')
def dashboard(request):
    return render(request,'adminlogin/dashboard.html')

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='login')
def usertable(request):
    dictionary={
        'members': User.objects.all().order_by('id')
    }
    return render(request,'adminlogin/usertable.html',dictionary)

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='login')
def adminproduct(request):
    dictionary={
        'prod': Product.objects.all().order_by('id')
    }
    return render(request,'adminlogin/adminproduct.html',dictionary)

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='login')
def addproduct(request):
    if request.method == 'POST':
        prod_name = request.POST['product_name']
        description = request.POST['description']
        categories = request.POST['categories']
        brand = request.POST['brand']
        image = request.FILES.get('image')
        stock = request.POST['stock']
        price = request.POST['price']
        try:
            is_super = request.POST['is_superuser']
        except: 
            is_super = False

        if prod_name.strip() == '' and description.strip() == '' and categories.strip() == '' and stock.strip() == '' and price.strip() == '':
            messages.error(request, "Fields can't be blank")
            return redirect('addproduct')   
        if Product.objects.filter(product_name=prod_name).exists():
            messages.error(request, 'Product already exists')
            return redirect('addproduct')
        cat = Categories.objects.get(product_name = categories)
        brnd = Brand.objects.get(brand_name=brand)
        prd = Product(product_name=prod_name,description=description,categories=cat,brand=brnd,image=image,stock=stock,price=price)  
        prd.save()
        messages.success(request, 'Product Added successfully')
        return redirect('adminproduct')
    return render(request,'adminlogin/add_product.html') 

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='login')
def deleteproduct(request,prod_id):
    prod = Product.objects.get(id=prod_id)
    prod.delete()
    messages.success(request,'Product Deleted successfully')
    return redirect('adminproduct')

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='login')
def editproduct(request,prod_id):
    if request.method =='POST':
        prod_name = request.POST['product_name']
        description = request.POST['description']
        categories = request.POST['categories']
        image = request.FILES.get('image')
        stock = request.POST['stock']
        price = request.POST['price']
        if prod_name == '' and description == '' and categories == '' and stock == '' and price == '':
            messages.error(request, "Fields can't be blank")
            return redirect('editproduct', prod_id)
        cat = Categories.objects.get(product_name = categories)   
        
        prd = Product.objects.get(id=prod_id)
        prd.product_name = prod_name
        prd.description = description
        prd.categories = cat
        if image:
            prd.image = image
        prd.stock = stock
        prd.price = price

        messages.success(request, 'Product updated successfully')
        prd.save()
        return redirect('adminproduct')
    prd = Product.objects.get(id=prod_id)
    return render(request, 'adminlogin/editproduct.html',{'prd': prd})           

def block_user(request,user_id):
    user_obj = User.objects.get(id = user_id)
    if user_obj.is_active:
        user_obj.is_active = False
        user_obj.save()
    else:
        user_obj.is_active = True
        user_obj.save()  
    return redirect('usertable') 




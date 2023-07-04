from django.shortcuts import render,redirect,HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.views.decorators.cache import cache_control
from django.contrib.auth.decorators import login_required
from product.models import Product,Categories,Brand,Offer
from order.models import Order,Ordered_Product
from datetime import datetime
from datetime import datetime, timedelta
from django.db.models import Sum
from django.db.models.functions import TruncDay
from django.db.models.functions import Cast
from django.db.models import DateField

# Create your views here.

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='login')
def dashboard(request):
    if not request.user.is_superuser:
        return redirect('login')

    delivered_items = Ordered_Product.objects.filter(status='Delivered')

    revenue = 0
    for item in delivered_items:
        revenue += item.order_id.total_amount

    top_selling = Ordered_Product.objects.annotate(total_quantity=Sum('quantity')).order_by('-total_quantity').distinct()[:5]

    recent_sale = Ordered_Product.objects.all().order_by('-id')[:5]

    today = datetime.today()
    date_range = 7

    four_days_ago = today - timedelta(days=date_range)

    orders = Order.objects.filter(order_date__gte=four_days_ago,order_date__lte=today)

    sales_by_day = orders.annotate(day=TruncDay('order_date')).values('day').annotate(total_sales=Sum('total_amount')).order_by('day')
    sales_dates = Order.objects.annotate(sale_date=Cast('order_date', output_field=DateField())).values('sale_date').distinct()

    context = {
        'total_users':User.objects.count(),
        'sales':Ordered_Product.objects.count(),
        'revenue':revenue,
        'top_selling':top_selling,
        'recent_sales':recent_sale,
        'sales_by_day':sales_by_day,
    }
    return render(request,'adminlogin/dashboard.html',context)




    # return render(request,'adminlogin/dashboard.html')

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
        price = request.POST['price']
        try:
            is_super = request.POST['is_superuser']
        except: 
            is_super = False

        if prod_name.strip() == '' or description.strip() == '' or categories.strip() == '' or price.strip() == '' or brand.strip() == '' or image == '':
            messages.error(request, "Fields can't be blank")
            return redirect('addproduct')   
        if Product.objects.filter(product_name=prod_name).exists():
            messages.error(request, 'Product already exists')
            return redirect('addproduct')
        cat = Categories.objects.get(id = categories)
        brnd = Brand.objects.get(id = brand)
        prd = Product(product_name=prod_name,description=description,categories=cat,brand=brnd,image=image,price=price)  
        prd.save()
        messages.success(request, 'Product Added successfully')
        return redirect('adminproduct')
    context={
        'cat' : Categories.objects.all(),
        'brand' : Brand.objects.all(),
        'offer' : Offer.objects.all(),
    }
    return render(request,'adminlogin/add_product.html',context) 

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
        brand = request.POST['brand']
        categories = request.POST['categories']
        image = request.FILES.get('image')
        price = request.POST['price']
        offer = request.POST['offer']
        if prod_name == '' or description == '' or categories == '' or price == '' or offer == '' or image == '':
            messages.error(request, "Fields can't be blank")
            return redirect('editproduct', prod_id)
        print(brand,"gggggggggggggggggggg")
        brnd = Brand.objects.get(brand_name = brand)
        cat = Categories.objects.get(product_name = categories)   
        offr = Offer.objects.get(name = offer)

        prd = Product.objects.get(id=prod_id)
        prd.product_name = prod_name
        prd.description = description
        prd.brand = brnd
        prd.categories = cat
        prd.offer = offr
        if image:
            prd.image = image
        prd.price = price

        messages.success(request, 'Product updated successfully')
        prd.save()
        return redirect('adminproduct')
    prd = Product.objects.get(id=prod_id)
    
    return render(request, 'adminlogin/editproduct.html',{'prd': prd,'cat' : Categories.objects.all(),'brand' : Brand.objects.all(),'offer' : Offer.objects.all()})           


def block_user(request,user_id):
    user_obj = User.objects.get(id = user_id)
    if user_obj.is_active:
        user_obj.is_active = False
        user_obj.save()
    else:
        user_obj.is_active = True
        user_obj.save()  
    return redirect('usertable') 




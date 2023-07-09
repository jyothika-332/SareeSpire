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
from openpyxl import Workbook
import io


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



@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='login')
def report(request):   
    context = {}
    if request.method == 'POST':
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        
       
        
        if start_date == '' or end_date == '':
            messages.error(request, 'Give date first')
            return redirect('report')
            
        if start_date == end_date:
            date_obj = datetime.strptime(start_date, '%Y-%m-%d')
            order_items = Order.objects.filter(total_amount__gt=0,order_date=date_obj.date())
            if order_items:
                context.update(sales=order_items, s_date=start_date, e_date=end_date)
                return render(request, 'adminlogin/salesreport.html', context)
            else:
                messages.error(request, 'No data found')
            return redirect('report')

        order_items = Order.objects.filter(total_amount__gt=0,order_date__gte=start_date, order_date__lte=end_date)
        total_revenue = order_items.aggregate(total_revenue=Sum('total_amount'))['total_revenue']
        
        if order_items:
            context.update(sales = order_items, s_date = start_date, e_date = end_date, total_revenue = total_revenue)
            
        else:
            messages.error(request, 'No data found')

    return render(request,'adminlogin/salesreport.html',context)



# EXCEL Sales Report 
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='login')
def sales_report_excel(request):  
    context = {} 
    if request.method == 'POST': 
        start_date = request.POST.get('Es_date') 
        end_date = request.POST.get('Ee_date') 
        
        if start_date == '' or end_date == '': 
            messages.error(request, 'Give date first') 
            return redirect('report')
        if start_date == end_date: 
            date_obj = datetime.strptime(start_date, '%Y-%m-%d') 
            order_items = Order.objects.filter(total_amount__gt=0,order_date=date_obj.date()) 
            if order_items: 
                context.update(sales=order_items, s_date=start_date, e_date=end_date) 
                return render(request, 'adminlogin/salesreport.html', context) 
            else: 
                messages.error(request, 'No data found') 
            return redirect('report') 
        order_items = Order.objects.filter(total_amount__gt=0,order_date__gte=start_date, order_date__lte=end_date) 
        total_revenue = order_items.aggregate(total_revenue=Sum('total_amount'))['total_revenue'] 
        if order_items: 
            context.update(sales = order_items,s_date = start_date, e_date = end_date, total_revenue = total_revenue)

            # EXCEL WORKS 
            sales_data = context 

            workbook = Workbook() 
            sheet=workbook.active 
            sheet.title='SalesData' 
                
            sheet['A1']='Order_Id' 
            sheet['B1']='time_of_order' 
            sheet['C1']='mode_of_payment' 
            sheet['D1']='total_amount' 
            
                
            row_num=4 
            for order in sales_data['sales']: 
                sheet[f'A{row_num}']=order.id 
                sheet[f'B{row_num}']=order.order_date.replace(tzinfo=None).strftime('%Y-%m-%d%H:%M:%S') 
                sheet[f'C{row_num}']=order.mode_of_payment 
                sheet[f'D{row_num}']=order.total_amount 
                row_num+=1 
                
            excel_file=io.BytesIO() 
            workbook.save(excel_file) 
            excel_file.seek(0) 
                
            response=HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet') 
            response['Content-Disposition']='attachment;filename="sales_data.xlsx"' 
            response['Content-Transfer-Encoding']='binary' 
            response.write(excel_file.read()) 
                
            return response 
        else: 
            messages.error(request,'No data found') 
    return render(request,'adminlogin/salesreport.html',context)




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
        prod_name = request.POST.get('product_name')
        description = request.POST.get('description')
        categories = request.POST.get('categories')
        brand = request.POST.get('brand')
        image = request.FILES.get('image')
        price = request.POST.get('price')
        try:
            is_super = request.POST.get('is_superuser')
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
        prod_name = request.POST.get('product_name')
        description = request.POST.get('description')
        brand = request.POST.get('brand')
        categories = request.POST.get('categories')
        image = request.FILES.get('image')
        price = request.POST.get('price')
        offer = request.POST.get('offer')

        if prod_name == '' or description == '' or categories == '' or price == '' or offer == '' or image == '':
            messages.error(request, "Fields can't be blank")
            return redirect('editproduct', prod_id)
        
        brnd = Brand.objects.get(id = brand)
        cat = Categories.objects.get(id = categories)   
        offr = Offer.objects.get(id = offer)

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
    
    try:
        prd = Product.objects.get(id=prod_id)
    except Product.DoesNotExist:
        return redirect(adminproduct)
    
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



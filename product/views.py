from django.shortcuts import render,get_object_or_404,redirect
from .models import Product, ColorVariation,Offer
from .models import Categories
from django.views.decorators.cache import cache_control
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib import messages
from django.db.models import Q

# Create your views here.

def productpage(request,category_slug = None):
    categories = None
    products = None
    if category_slug != None:
        categories = get_object_or_404(Categories,slug = category_slug)

        products = Product.objects.filter(categories=categories)
        product_count = products.count()
    else:
        products = Product.objects.all()  
        product_count = products.count() 


    dictionary= {
        'products': products,
        'product_count': product_count,
    }
    return render(request,'product/products.html',dictionary)


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def productdetails(request, category_slug, product_slug):
    products = Product.objects.filter(categories__slug=category_slug, slug=product_slug)
    single_product = products.first() 
    variations = ColorVariation.objects.filter(product=single_product)
    
    context = {
        'single_product': single_product,
        'variants' : variations
    }

    return render(request, 'product/singleproduct.html', context)


def change_variant(request):
    if request.method == 'POST':
        color = request.POST['variant']
        return JsonResponse({'variant':color})
    


# Product Search
def product_search(request):
    key = request.GET.get('key')

    products = Product.objects.filter(Q(brand__brand_name__icontains=key) |Q(product_name__icontains=key) | Q(categories__product_name__icontains=key) | Q(description__icontains=key))  
    product_count = products.count()
    
    dictionary= {
        'products': products,
        'product_count': product_count,
    }
    return render(request,'product/products.html',dictionary)



def adminoffer(request):
    context ={
        'offer': Offer.objects.all()
    }
    return render(request,'product/adminoffer1.html',context)



@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='login')
def addoffer(request):
    if request.method == 'POST':
        offer = request.POST['offer']
        discount = request.POST['discount']
        start_date = request.POST['start_date']
        end_date = request.POST['end_date']
        try:
            is_super = request.POST['is_superuser']
        except: 
            is_super = False

        if offer.strip() == '' or discount.strip() == '' or start_date.strip() == '' or end_date.strip() == '':
            messages.error(request, "Fields can't be blank")
            return redirect('addoffer')   
        if Offer.objects.filter(name=offer).exists():
            messages.error(request, 'Offer already exists')
            return redirect('addoffer')
        offr = Offer(name=offer,discount=discount,start_date=start_date,end_date=end_date)  
        offr.save()
        messages.success(request, 'Offer Added successfully')
        return redirect('adminoffer')
    return render(request,'product/addoffer.html') 



@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='login')
def editoffer(request,offer_id):
    if request.method =='POST':
        offer = request.POST['offer']
        discount = request.POST['discount']
        start_date = request.POST['start_date']
        end_date = request.POST['end_date']
        if offer == '' or discount == '' or start_date == '' or end_date == '':
            messages.error(request, "Fields can't be blank")
            return redirect('editoffer', offer_id)   
        
        offr = Offer.objects.get(id=offer_id)
        offr.name = offer
        offr.discount = discount
        offr.start_date = start_date
        offr.end_date = end_date

        messages.success(request, 'Offer updated successfully')
        offr.save()
        return redirect('adminoffer')
    try:
        offr = Offer.objects.get(id=offer_id)
    except Offer.DoesNotExist:
        return redirect(adminoffer)
    
    return render(request, 'product/editoffer.html',{'offr': offr})


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='login')
def deleteoffer(request,offer_id):
    offr = Offer.objects.get(id=offer_id)
    offr.delete()
    messages.success(request,'Offer Deleted successfully')
    return redirect('adminoffer')
from django.shortcuts import render,get_object_or_404
from .models import Product, ColorVariation
from .models import Categories
from django.views.decorators.cache import cache_control
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

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
@login_required(login_url='login')
def productdetails(request, category_slug, product_slug):
    products = Product.objects.filter(categories__slug=category_slug, slug=product_slug)
    single_product = products.first() 
    variations = ColorVariation.objects.filter(product=single_product)
    
    context = {
        'single_product': single_product,
        'variants' : variations
    }

    # if request.GET.get('variant'):
    #     color = request.GET.get('variant')
    #     selected_variant = ColorVariation.objects.get(product=single_product,color=color)
    #     print(selected_variant.color,"selected here")

    #     context['selected_variant'] = selected_variant
    return render(request, 'product/singleproduct.html', context)


def change_variant(request):
    if request.method == 'POST':
        color = request.POST['variant']
        return JsonResponse({'variant':color})
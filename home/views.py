from django.shortcuts import render
from home.models import Ads
from product.models import Product, Categories
from django.views.decorators.cache import cache_control
from django.contrib.auth.decorators import login_required

# Create your views here.

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def homepage(request):
    ads = {
        'ads' : Ads.objects.all(),
        'catergory': Categories.objects.all(),
    }
    return render(request,'homepage/homepage.html',ads)
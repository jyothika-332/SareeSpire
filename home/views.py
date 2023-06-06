from django.shortcuts import render
from home.models import Ads

# Create your views here.

def homepage(request):
    ads = {
        'ads' : Ads.objects.all()
    }
    return render(request,'homepage/homepage.html',ads)
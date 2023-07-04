from django.shortcuts import render,redirect
from product.models import Product,ColorVariation
from django.views.decorators.cache import cache_control
from django.contrib.auth.decorators import login_required
from wishlist.models import Wishlist
from django.contrib import messages
from cart.models import Cart,CartItem

# Create your views here.

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='login')
def wishlist(request):
    wishlistitems = Wishlist.objects.filter(users =request.user)
    
    context = {
        'wishlistitems' : wishlistitems,
    }
    return render(request,'wishlist/wishlist.html',context)

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='login')
def add_to_wishlist(request,id):
    variant = request.GET.get('variant')
    color_variant = ColorVariation.objects.get(id = variant)
    product = Product.objects.get(id = id)
    exist = Wishlist.objects.filter(users=request.user, product__id = id)
    # prd = ColorVariation.objects.get(id=id)
    if not exist:
        obj=Wishlist(users=request.user,product=color_variant)
        obj.save()
    else:
        messages.success(request,'Item Already Existed')    
        
    return redirect(wishlist)


def wishlist_remove(request,id):
    product = Wishlist.objects.get(id=id)
    product.delete()
    return redirect('wishlist')


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='login')
def add_to_cart(request):
    variant = request.GET.get('variant_id')
    prd = request.GET.get('product_id')
    color_variant = ColorVariation.objects.get(id = variant)
    product = Product.objects.get(id = prd)
    user = request.user
    cart,_ = Cart.objects.get_or_create(users=user, is_paid = False)
    is_cart_item_exists = CartItem.objects.filter(cart=cart,product=product, color=color_variant).exists()
    print(is_cart_item_exists)

    if is_cart_item_exists:
        cart_item = CartItem.objects.get(cart=cart,product=product, color=color_variant)
        cart_item.quantity += 1
        cart_item.save()
    else:
        cart_item = CartItem.objects.create(cart=cart,product=product, color=color_variant)

    return redirect('cart')


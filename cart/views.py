from django.shortcuts import render, redirect
from product.models import Product,ColorVariation
from cart.models import *
from django.http import HttpResponseRedirect

# Create your views here.
def cart(request):
    cart = Cart.objects.get(users=request.user, is_paid=False)
    cart_items = CartItem.objects.filter(cart=cart)
    context ={
        'cartitem':cart_items
    }
    return render(request,'cart/cart.html',context)


def add_to_cart(request,id):
    variant = request.GET.get('variant')
    color_variant = ColorVariation.objects.get(id = variant)
    product = Product.objects.get(id = id)
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
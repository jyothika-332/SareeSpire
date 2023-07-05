from django.shortcuts import render, redirect
from product.models import Product,ColorVariation
from cart.models import *
from django.http.response import JsonResponse
from django.views.decorators.cache import cache_control
from django.contrib.auth.decorators import login_required
from django.contrib import messages


# Create your views here.

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='login')
def cart(request):
    try:
        cart = Cart.objects.get(users=request.user, is_paid=False)
    except Cart.DoesNotExist:
        return render(request,'cart/cart.html')
    cart_items = CartItem.objects.filter(cart=cart)
    total_price = 0
    tax = 0
    grand_total =0
    single_product_total = [0]
    for item in cart_items:
        grand_total = total_price + tax
        if item.product.offer:
            total_price = total_price + item.product.get_offer_price() * item.quantity
            single_product_total.append(item.product.get_offer_price() * item.quantity)
            tax = total_price * 0.18
            grand_total = total_price + tax
        else:    
            total_price = total_price + item.product.price * item.quantity
            single_product_total.append(item.product.price * item.quantity)
            tax = total_price * 0.18
            grand_total = total_price + tax

    context ={
        'cartitem':cart_items,
        'total_price' : total_price,
        'single_product_total':single_product_total,
        'grand_total':grand_total,
        'tax' : tax,
        'cart' :cart,
    }
    return render(request,'cart/cart.html',context)


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='login')
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
        if product.offer:
            total = product.get_offer_price()
        else:
            total = product.price
        cart_item = CartItem.objects.create(cart=cart,product=product, color=color_variant,price = total)

    return redirect('cart')

@cache_control(no_cache=True,must_revalidate=True,no_store=True)
@login_required(login_url='signin')
def update_cart(request):
    if request.method == 'POST':
        variant_id = request.POST.get('variant_id')
        if (CartItem.objects.filter(color=variant_id)):
            prod_qty = request.POST.get('product_qty')
            cart = CartItem.objects.get(color=variant_id)
            cartes = cart.color.quantity
            cart_id = cart.cart.id
            print(cart_id)
            if int(cartes) >= int(prod_qty):
                cart.quantity = prod_qty
                cart.save()
                    
                carts = CartItem.objects.filter(cart=cart_id).order_by('id')
                total_price = 0
                for item in carts:
                    if item.product.offer:
                        item.price = item.product.get_offer_price() * item.quantity
                        item.save()
                        total_price = total_price + item.product.get_offer_price() * item.quantity
                    else:    
                        item.price=item.product.price * item.quantity
                        item.save()
                        total_price = total_price + item.product.price * item.quantity
                return JsonResponse({'status': 'Updated successfully','sub_total':total_price,})
            else:
                return JsonResponse({'status': 'Not quantity'})
    return JsonResponse('something went wrong, reload page',safe=False)

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='login')
def deleteitem(request,cart_id):
    cartitem = CartItem.objects.get(id=cart_id)
    cartitem.delete()
    messages.success(request,'Item Deleted successfully')
    return redirect('cart')

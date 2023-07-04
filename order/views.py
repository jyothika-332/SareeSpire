from django.shortcuts import render,redirect
from django.views.decorators.cache import cache_control
from django.contrib.auth.decorators import login_required
from order.models import Order,Ordered_Product,Returned
from django.contrib import messages
from django.http import HttpResponseRedirect

# Create your views here.


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='login')
def mainorderpage(request):
    context={
        'orders': Order.objects.filter(customer=request.user)
    }
    return render(request,'orders/mainorder.html',context)



@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='login')
def order(request,order_item_id):
    context={
        'orders': Ordered_Product.objects.filter(order_id__id=order_item_id)
    }
    return render(request,'orders/orders.html',context)


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='login')
def adminorder(request):
    context={
        'orders': Order.objects.all()
    }
    return render(request,'orders/adminorders.html',context)


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='login')
def update_status(request, order_item_id):
    order_item = Ordered_Product.objects.get(id=order_item_id)

    if request.method == 'POST':
        status = request.POST.get('status')
        order_item.status = status
        order_item.save()
        return redirect('adminorder')
    


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='login')
def cancel_order(request,order_item_id):
   customer = request.user
   ord_prod = Ordered_Product.objects.get(id=order_item_id)
   
   
   ord_prod.status = 'Cancelled' 
   if ord_prod.order_id.mode_of_payment != "COD":
        customer.wallet = customer.wallet + ord_prod.amount
   ord_prod.product.quantity += ord_prod.quantity
   ord_prod.order_id.total_amount -= ord_prod.amount
   ord_prod.order_id.save()
   ord_prod.product.save()
   ord_prod.save()
   customer.save()


   messages.error(request,'Order Cancelled..!!')
   if ord_prod.order_id.mode_of_payment != "COD":
        messages.error(request,'Amount Refunded to your Wallet..!!')
   return HttpResponseRedirect(request.META.get('HTTP_REFERER'))    


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='login')
def adminsingleorder(request,order_item_id):
    context={
        'orders': Ordered_Product.objects.filter(order_id=order_item_id)
    }
    return render(request,'orders/adminsingleorder.html',context)


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='login')
def return_item(request):
    if request.method == 'POST':
        ordr_id = request.POST.get('item')
        reason = request.POST.get('return_reason')
        comment = request.POST.get('return_comment')

        returned_product = Ordered_Product.objects.get(order_id=ordr_id)
        Returned.objects.create(returned_product=returned_product,reason=reason,comments=comment)

        returned_product.status = 'Returned'

        if returned_product.order_id.mode_of_payment != 'COD':
            request.user.wallet += returned_product.amount

        returned_product.save()
        request.user.save()

        if reason == 'Ordered by mistake' or 'Wrong item':
               returned_product.product.quantity += returned_product.quantity
               returned_product.product.save()

        messages.error(request,'Item return initiated, will be processed in 2 days, please see the amount in your Wallet..')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))       
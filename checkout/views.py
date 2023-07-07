from django.shortcuts import render,redirect
from userprofile.models import UserAddress
from django.views.decorators.cache import cache_control
from django.contrib.auth.decorators import login_required
from cart.models import Cart,CartItem
from order.models import Order,Ordered_Product
from django.contrib import messages
from django.http import JsonResponse
from checkout.models import Coupon,CouponUsed


# Create your views here.



@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='login')
def checkout(request):
    cart = Cart.objects.get(users=request.user, is_paid=False)
    cart_items = CartItem.objects.filter(cart__id=cart.id)
    if not cart_items:
        return redirect('product')
    else:
        total_price = 0
        for item in cart_items:
            if item.product.offer:
                total_price = total_price + item.product.get_offer_price() * item.quantity
                tax = total_price * 0.18
                grand_total = total_price + tax
            else:    
                total_price = total_price + item.product.price * item.quantity
                tax = total_price * 0.18
                grand_total = total_price + tax

        address = UserAddress.objects.filter(customer_id=request.user)
        context = {
            'customer': address,
            'addresses': address,
            'cartitem':cart_items,
            'total_price' : total_price,
            'grand_total':grand_total,
            'tax' : tax,
        }

        return render(request,'checkout/checkout.html',context)


@cache_control(no_cache=True, must_revalidate=True, no_store=True)     
@login_required(login_url='login')
def place_order(request):
    user= request.user
    if request.method == 'POST':
        mode_of_payment = request.POST.get('payment')
        selected_address = request.POST.get('address')
        new_price = request.POST.get('new_price')
        coupon_code2 = request.POST.get('coupon_code2')
        if not mode_of_payment:
            messages.error(request,'Please select a payment method..!!')
            return redirect('checkout')  
                  
        if selected_address:
            address = UserAddress.objects.get(id=selected_address)
        else:    
            messages.error(request,'Please select an address..!!')
            return redirect('checkout')
            
        ordered_products = CartItem.objects.filter(cart__users = request.user)
        print(ordered_products)
        if ordered_products:
            amount = 0
            for i in ordered_products:
                if i.product.offer:
                    amount = amount + i.product.get_offer_price() * i.quantity
                    tax = amount * 0.18
                    grand_total = amount + tax
                    i.color.quantity = i.color.quantity - i.quantity
                    i.color.save()
                else:
                    amount = amount + i.product.price * i.quantity
                    tax = amount * 0.18
                    grand_total = amount + tax
                    i.color.quantity = i.color.quantity - i.quantity
                    i.color.save()

            if new_price:
                amount = new_price    

            order = Order(customer = user, address=address, mode_of_payment=mode_of_payment, total_amount=grand_total)
            order.save()

            if new_price:
                CouponUsed.objects.create(coupon = Coupon.objects.filter(coupon_code=coupon_code2).first(),order=order)
            
            for item in ordered_products:
                object=Ordered_Product(order_id=order, product=item.color, quantity=item.quantity, amount=item.product.price)
                object.save()
                item.delete()
            payMode = request.POST.get('payment')
            if (payMode == "Paid_by_Razorpay"):
                return JsonResponse({'status':"Your Order has been placed successfully"})    

            if mode_of_payment == 'COD':    
                messages.info(request,'Order Placed')
                return render(request,'checkout/confirmation.html',{"order":order, "products": Ordered_Product.objects.filter(order_id=order.id),"address":UserAddress.objects.filter(customer_id=user.id)})
            
        else:
            messages.error(request,'Cannot place an order. Your Cart is empty..!!')
            return redirect('checkout')
                   
    return redirect('checkout') 


@login_required(login_url='login')
def razorpaycheck(request):
    new_price = request.GET.get('new_price')
    coupon_code2 = request.GET.get('coupon_code2')
    
    cart = Cart.objects.get(users=request.user)
    cart_items = CartItem.objects.filter(cart__id=cart.id)
    total_price = 0
    tax = 0
    grand_total =0

    for item in cart_items:
        total_price = total_price + item.product.price * item.quantity 
        tax = total_price * 0.18
        grand_total = total_price + tax

    if new_price:
        grand_total = new_price    

    return JsonResponse({'total_price': grand_total,'coupon_code2':coupon_code2}) 



@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='login')
def checkout_add_address(request):
    if request.method == 'POST':
        house_name = request.POST['house_name']
        city = request.POST['city']
        state = request.POST['state']
        country = request.POST['country']
        phone = request.POST['phone']
        pincode = request.POST['pincode']
        

        if house_name.strip() == '' or city.strip() == '' or state.strip() == '' or country.strip() == '' or phone.strip() == '' or pincode.strip() == '':
            messages.error(request, "Fields can't be blank")
            return redirect('addaddress')   
        if UserAddress.objects.filter(housename=house_name).exists():
            messages.error(request, 'Address already exists')
            return redirect('addaddress')
        address = UserAddress(customer_id=request.user,housename=house_name,city=city,state=state,country=country,phone=phone,pincode=pincode)  
        address.save()
        messages.success(request, 'Address Added successfully')
        return redirect('checkout')
    return render(request,'checkout/checkout.html')


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='login')
def confirmation(request):
    user= request.user
    
    if request.method == 'POST':
        mode_of_payment = request.POST.get('payment')
        selected_address = request.POST.get('address')
        if selected_address:
            address = UserAddress.objects.get(id=selected_address)

        ordered_products = CartItem.objects.filter(cart__users = request.user)
        if ordered_products:
            amount = 0
            for i in ordered_products:
                if i.product.offer:
                    amount = amount + i.product.get_offer_price() * i.quantity
                    i.color.quantity = i.color.quantity - i.quantity
                    i.color.save()
                else:
                    amount = amount + i.product.price * i.quantity
                    i.color.quantity = i.color.quantity - i.quantity
                    i.color.save()

        order = Order(customer = user, address=address, mode_of_payment=mode_of_payment, total_amount=amount)
        order.save()
        context = {
            "order":order, 
            "products": Ordered_Product.objects.filter(order_id=order.id),
            "address":UserAddress.objects.filter(customer_id=user.id),
        }

        return render(request,'confirmation.html',context)

    

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='login')
def apply_coupon(request):
    if request.method == 'POST':
        coupon_code = request.POST.get('coupon_code')
        order_total = request.POST.get('order_total')
        order_total = float(order_total)
        coupon = Coupon.objects.filter(coupon_code=coupon_code).first()

        if coupon:
            coupon_used = CouponUsed.objects.filter(order__customer=request.user,coupon__id=coupon.id)
            if coupon_used:
                return JsonResponse({'status': 'Coupon already used..'})
            else:
                if order_total>coupon.minimum_purchase:
                    new_total = order_total - coupon.discount
                    return JsonResponse({'status': 'Coupon Applied..!!','new_total':new_total,'coupon_discount':coupon.discount, 'coupon_code':coupon_code})
                else:
                   return JsonResponse({'status': 'You can not use this coupon..'}) 
        else:
            return JsonResponse({'status': 'Coupon does not exist..'})
        


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='login')
def admincoupon(request):
    context = {
        'coupon' : Coupon.objects.all()
    }
    return render(request,'checkout/admincoupon.html',context)        



@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='login')
def addcoupon(request):
    if request.method == 'POST':
        coupon_code = request.POST['coupon_code']
        discount = request.POST['discount']
        minimum_purchase = request.POST['minimum_purchase']

        if coupon_code.strip() == '' or discount.strip() == '' or minimum_purchase.strip() == '':
            messages.error(request, "Fields can't be blank")
            return redirect('addcoupon')  
        if Coupon.objects.filter(coupon_code=coupon_code).exists():
            messages.error(request, 'Coupon already exists')
            return redirect('addcoupon')

        cpn = Coupon(coupon_code=coupon_code,discount=discount,minimum_purchase=minimum_purchase) 
        cpn.save()
        messages.success(request, 'Coupon Added successfully')
        return redirect('admincoupon') 
    return render(request, 'checkout/addcoupon.html')


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='login')
def editcoupon(request,cpn_id):
    if request.method == 'POST':
        coupon_code = request.POST['coupon_code']
        discount = request.POST['discount']
        minimum_purchase = request.POST['minimum_purchase']

        if coupon_code.strip() == '' or discount.strip() == '' or minimum_purchase.strip() == '':
            messages.error(request, "Fields can't be blank")
            return redirect('editcoupon',cpn_id)
        
        cpn = Coupon.objects.get(id=cpn_id)
        cpn.coupon_code = coupon_code
        cpn.discount = discount
        cpn.minimum_purchase =minimum_purchase

        messages.success(request, 'Coupon updated successfully')
        cpn.save()
        return redirect('admincoupon')
    
    try:
        cpn = Coupon.objects.get(id=cpn_id)
    except Coupon.DoesNotExist:
        return redirect(admincoupon)
    
    return render(request, 'checkout/editcoupon.html',{'cpn': cpn})
            


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='login')
def deletecoupon(request,cpn_id):
    cpn = Coupon.objects.get(id=cpn_id)
    cpn.delete()
    messages.success(request,'Coupon Deleted successfully')
    return redirect('admincoupon')
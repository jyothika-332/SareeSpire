from django.shortcuts import render,redirect
from django.views.decorators.cache import cache_control
from django.contrib.auth.decorators import login_required
from product.models import Categories,ColorVariation,Product
from django.contrib import messages
# Create your views here.


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='login')
def admincategory(request):
    context={
        'cat': Categories.objects.all()
    }
    return render(request,'category/admincategory.html',context)


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='login')
def addcategory(request):
    if request.method == 'POST':
        category_name = request.POST['category_name']
        description = request.POST['description']
        image = request.FILES.get('image')
        try:
            is_super = request.POST['is_superuser']
        except: 
            is_super = False

        if category_name.strip() == '' or description.strip() == '' or image == '':
            messages.error(request, "Fields can't be blank")
            return redirect('addcategory')
        if not image:
            messages.error(request, "Image not found")
            return redirect('addcategory') 
          
        if Categories.objects.filter(product_name=category_name).exists():
            messages.error(request, 'Category already exists')
            return redirect('addcategory')
        cat = Categories(product_name=category_name,description=description,image=image)  
        cat.save()
        messages.success(request, 'Category Added successfully')
        return redirect('admincategory')
    return render(request,'category/addcategory.html') 


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='login')
def deletecategory(request,cat_id):
    prod = Categories.objects.get(id=cat_id)
    prod.delete()
    messages.success(request,'Category Deleted successfully')
    return redirect('admincategory')



@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='login')
def editcategory(request,cat_id):
    if request.method =='POST':
        category_name = request.POST['category_name']
        description = request.POST['description']
        image = request.FILES.get('image')
        if category_name == '' or description == '':
            messages.error(request, "Fields can't be blank")
            return redirect('editcategory', cat_id)
        if not image:
            messages.error(request, "Image not found")
            return redirect('editcategory', cat_id)
        
        cat = Categories.objects.get(id=cat_id)
        cat.product_name = category_name
        cat.description = description
        if image:
            cat.image = image
        messages.success(request, 'category updated successfully')
        cat.save()
        return redirect('admincategory')
    
    try:
        cat = Categories.objects.get(id=cat_id)
    except Categories.DoesNotExist:
        return redirect(admincategory)
    
    return render(request, 'category/editcategory.html',{'cat': cat})



@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='login')
def adminvariation(request):
    context ={
        'var': ColorVariation.objects.all()
    }
    return render(request,'category/adminvariation.html',context)



@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='login')
def add_variation(request):
    if request.method == 'POST':
        product = request.POST['product']
        description = request.POST['description']
        color = request.POST['color']
        image = request.FILES.get('image')
        quantity = request.POST['quantity']        
        try:
            is_super = request.POST['is_superuser']
        except: 
            is_super = False

        if product.strip() == '' or description.strip() == '' or image == '' or color.strip() == '' or quantity.strip() == '':
            messages.error(request, "Fields can't be blank")
            return redirect('add_variation') 
        if not image:
            messages.error(request, "Image not found")  
            return redirect('add_variation')
        if ColorVariation.objects.filter(product=product,color=color).exists():
            messages.error(request, 'This product variation already exists')
            return redirect('add_variation')
        
        product = Product.objects.get(id=product)
        vartn = ColorVariation(product=product,description=description,color=color,image=image,quantity=quantity)  
        vartn.save()
        messages.success(request, 'Product variation Added successfully')
        return redirect('admin_variation')
    
    context={
        'prd' : Product.objects.all(),
    }
    
    return render(request,'category/add_variation.html',context)



@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='login')
def edit_variation(request,var_id):
    if request.method =='POST':
        product = request.POST['product']
        description = request.POST['description']
        color = request.POST['color']
        quantity = request.POST['quantity']
        image = request.FILES.get('image',None)
        if product == '' or description == '' or color == '' or quantity == '':
            messages.error(request, "Fields can't be blank")
            return redirect('edit_variation', var_id)
        if not image:
            messages.error(request, "Image not found")
            return redirect('edit_variation', var_id)
        prd = Product.objects.get(id=product)
        vartn = ColorVariation.objects.get(id=var_id)
        vartn.product = prd
        vartn.description = description
        if image:
            vartn.image = image
        vartn.color = color
            
        messages.success(request, 'Product variation updated successfully')
        vartn.save()
        return redirect('admin_variation')
    
    try:
        vartn = ColorVariation.objects.get(id=var_id)
    except ColorVariation.DoesNotExist:
        return redirect('admin_variation')
    
    return render(request, 'category/edit_variation.html',{'vartn': vartn,'product':Product.objects.all(),})



@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='login')
def delete_variation(request,var_id):
    vartn = ColorVariation.objects.get(id=var_id)
    vartn.delete()
    messages.success(request,'Product Variation Deleted successfully')
    return redirect('admin_variation')
from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from cart_app.models import Order,OrderItem
from store.models import FarmerProfile  

@login_required
def admin_dashboard(request):
    if not request.user.is_staff:
        return redirect('index')

    customers = User.objects.filter(is_staff=False)
    farmers = FarmerProfile.objects.all()
    orders = Order.objects.all()

    context = {
        'customers': customers,
        'farmers': farmers,
        'orders': orders,
    }

    return render(request, 'admin_dashboard.html', context)
@login_required
def farmer_detail(request,farmer_id):
    farmer=get_object_or_404(FarmerProfile,id=farmer_id)
    order_items = OrderItem.objects.filter(product__farmer=farmer)

    products_data={}
    for item in order_items:
        prod = item.product
        if prod.id not in products_data:
            products_data[prod.id] = {
                'product': prod,
                'orders': []
            }
        products_data[prod.id]['orders'].append(item)

    return render(request, 'farmer_detail.html', {
        'farmer': farmer,
        'products_data': products_data.values()  # list of products with orders
    })
    

@login_required
def accept_farmer(request,farmer_id):
    if request.user.is_staff:
        farmer=FarmerProfile.objects.get(id=farmer_id)
        farmer.is_verified = True
        farmer.save()
    return redirect('admin_dashboard')

@login_required
def block_farmer(request,farmer_id):
    if request.user.is_staff:
        farmer = FarmerProfile.objects.get(id=farmer_id)
        farmer.is_verified=False
        farmer.save()
    return redirect('admin_dashboard')
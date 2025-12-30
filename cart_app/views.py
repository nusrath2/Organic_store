from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import CartItem,Order,OrderItem
from store.models import Product,FarmerProfile,Review
from store.forms import RatingForm

# Create your views here.
@login_required
def cart_home(request):
    items = CartItem.objects.filter(user=request.user)
    total = sum(item.total_price() for item in items)
    return render(request, 'cart.html', {'items': items, 'total': total})

def addtocart(request, pid):
    product = get_object_or_404(Product, id=pid)

    if not request.user.is_authenticated:
         return render (request,'login_required_cart.html',{'product' : product})

    if product.stock <= 0:
         return redirect('proinfo',pid=product.id)
    
    cart_item, created = CartItem.objects.get_or_create(user=request.user, product=product)

    if cart_item.quantity<product.stock:
         cart_item.quantity +=1
         cart_item.save()
         
    return redirect('cart_home')

@login_required
def update_cart(request, item_id):
    cart_item=get_object_or_404(CartItem,id=item_id,user=request.user)
    quantity=int(request.GET.get('quantity',cart_item.quantity))

    if quantity> 0:
            cart_item.quantity=quantity
            cart_item.save()
    else:
            cart_item.delete()

    return redirect('cart_home')

def remove_from_cart(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id, user=request.user)
    cart_item.delete()
    return redirect('cart_home')


def place_order(request):
    cart_items=CartItem.objects.filter(user=request.user)
    if not cart_items.exists():
          return redirect('cart_home')
    order=Order.objects.create(user=request.user,
                               total_amount=sum(item.total_price()for item in cart_items),
                               status = 'Pending')
    for item in cart_items:
          product=item.product
          if product.stock >=item.quantity:
               product.stock -=item.quantity
               product.save()
          OrderItem.objects.create(order=order,product=item.product,price=item.product.price,quantity=item.quantity)
    item.delete()

    return redirect('payment_page',order_id=order.id)

@login_required
def payment_page(request,order_id):
     order=get_object_or_404(Order,id=order_id,user=request.user)
     grand_total = sum(item.price * item.quantity for item in order.items.all())
     return render(request,'payment.html',{'order':order , 'grand_total' : grand_total})

def process_payment(request,order_id):
     order=get_object_or_404(Order,id=order_id,user=request.user)

     if request.method == 'POST':
          payment_method= request.POST.get('payment_method')
          if payment_method:
            if payment_method == 'COD':
                order.payment_status = 'Pending'
                order.status = 'Processing'
            else:
                 order.payment_status = 'Paid'
                 order.status = 'Processing'
            order.save()

     return redirect('payment_success',order_id=order.id)

@login_required
def payment_success(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    items = order.items.all()

    if request.method == "POST":
       
        for item in items:
            
            product_rating_str = request.POST.get(f'product_rating_{item.id}')
            if product_rating_str:
                try:
                    product_rating = int(product_rating_str)
                    product = item.product
                    total_rating = float(product.rating) * getattr(product, 'rating_count', 0)
                    product.rating_count = getattr(product, 'rating_count', 0) + 1
                    product.rating = (total_rating + product_rating) / product.rating_count
                    product.save()
                except ValueError:
                    pass

           
            farmer_rating_str = request.POST.get(f'farmer_rating_{item.id}')
            if farmer_rating_str:
                try:
                    farmer_rating = int(farmer_rating_str)
                    farmer = item.product.farmer
                    total_rating = float(farmer.rating) * getattr(farmer, 'rating_count', 0)
                    farmer.rating_count = getattr(farmer, 'rating_count', 0) + 1
                    farmer.rating = (total_rating + farmer_rating) / farmer.rating_count
                    farmer.save()
                except ValueError:
                    pass

        # customer review
        comment = request.POST.get('comment')
        if comment:
                if not Review.objects.filter(user=request.user).exists():
                    Review.objects.create(
                        user=request.user,
                        comment=comment)
        return redirect('allproducts_all')

    return render(request, 'payment_success.html', {'order': order, 'items': items})

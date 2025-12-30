from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from . forms import UserRegisterForm,FarmerProfileForm,CustomerProfileForm,ProductForm
from . models import FarmerProfile,CustomerProfile,Product,Category,Review
from cart_app.models import Order,OrderItem
from django.contrib.auth.models import User
# Create your views here.

def home(request):
    return render(request, 'index.html')

def about(request):
    return render(request, 'about.html')

def features(request):
    return render(request, 'feature.html')

def contact(request):
    return render(request, 'contact.html')

def ourservices(request):
    return render(request,'ourservices.html')


def register(request):
    if request.method =='POST':
        user_form = UserRegisterForm(request.POST)

        if user_form.is_valid():
            user = user_form.save(commit=False)
            user.set_password(user_form.cleaned_data["password"])
            user.save()

            role=user_form.cleaned_data['role']

            if role=='farmer':
                FarmerProfile.objects.create(user=user,name=user.username)
            
            else:
                CustomerProfile.objects.create(user=user,name=user.username)
            
            return redirect('login_page')
        
    else:
        user_form=UserRegisterForm()
    return render(request,'register.html',{'form': user_form})

def login_page(request):
    error=""

    if request.user.is_authenticated:
        if request.user.is_staff:
            return redirect('admin_dashboard')
        
        elif FarmerProfile.objects.filter(user=request.user).exists():
            return redirect('farmer_dashboard')
        else:
            return redirect('customer_home')

    if request.method == 'POST':
        a=request.POST.get("username")
        b=request.POST.get("password")

        user=authenticate(request,username=a,password=b)

        if user:
            login(request,user)

            if user.is_staff:
                return redirect('admin_dashboard')

            elif FarmerProfile.objects.filter(user=user).exists():
                return redirect('farmer_dashboard')
            else:
                return redirect('customer_home')
            
        else:
            error="Invalid username or password"
            
    return render (request,'login.html',{'error': error})

def logout_user(request):
    logout(request)
    return redirect('index')

#--FARMER DASHBOARD--#
from django.contrib.auth.decorators import login_required
from .models import Product

@login_required
def farmer_dashboard(request):
    
    if not FarmerProfile.objects.filter(user=request.user).exists():
        return redirect('login_page')
    
    farmer=request.user.farmerprofile
    products=Product.objects.filter(farmer=farmer)

    context={
        'farmer':farmer,
        'products':products,
    }
    return render(request,'farmer_dashboard.html', context)

def products_by_category(request,cid):
    selected_category= get_object_or_404(Category,id=cid)
    products=Product.objects.filter(category=selected_category)
    categories=Category.objects.all()
    context={
        'products': products ,
        'categories' : categories,
        'selected_category': selected_category}
    return render(request,'customer_home.html',context)

def allproduct(request):
    pro=Product.objects.all()
    print(pro)
    return render(request,'product.html',{'pro':pro})

def allproducts_all(request):
    products=Product.objects.all()
    return render(request,'allproducts_all.html',{'products':products})

def proinfo(request,pid):
    pro=get_object_or_404(Product,id=pid)
    rating_percent=(float(pro.rating)/5) * 100
    return render(request,'proinfo.html',{'pro':pro , 'rating_percent' : rating_percent})

@login_required
def add_product(request):
    farmer = request.user.farmerprofile

    if request.method =='POST':
        form=ProductForm(request.POST,request.FILES)
        if form.is_valid():
            product=form.save(commit=False)
            product.farmer = farmer
            product.save()
            return redirect('farmer_dashboard')
    else:
        form=ProductForm()

    return render(request,'addpro.html',{'form':form})

def pro_edit(request,pid):
    pro=Product.objects.get(id=pid)

    if request.method =='POST':
        form=ProductForm(request.POST,request.FILES,instance=pro)
        if form.is_valid():
            form.save()
        return redirect('farmer_dashboard')
    else:
        form=ProductForm(instance=pro)
    return render(request,'proedit.html',{'pro': pro ,'form' : form})

def pro_delete(request,pid):
    pro=Product.objects.get(id=pid)

    if request.method =='POST':
        pro.delete()
        return redirect('farmer_dashboard')
    
    return render(request,'prodel.html',{'pro':pro})

#customer
def customer_home(request):
    products=Product.objects.all()
    categories=Category.objects.all()
          
    return render(request,'customer_home.html',{'products' : products,'categories': categories,'user': request.user})

#review page 
def customer_review(request):
    reviews=Review.objects.all().order_by('-created_at')
    return render(request,'customer_review.html',{'reviews': reviews})

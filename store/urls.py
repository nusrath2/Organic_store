from django.urls import path
from.import views
from django.contrib.auth.views import LogoutView,LoginView
urlpatterns = [
    path('',views.home,name="index"),
    path('about/', views.about, name='about'),
    path('features/', views.features, name='features'),
    path('contact/', views.contact, name='contact'),
    path('ourservices/',views.ourservices,name='ourservices'),

    path('register/',views.register,name='register'),
    path('login/',views.login_page,name='login_page'),
    path('logout/',views.logout_user,name='logout' ),
    path('allproducts_all',views.allproducts_all,name='allproducts_all'),
    
    #farmer dashboard
    path('farmer_dashboard/',views.farmer_dashboard,name='farmer_dashboard'),
    
    #public product pages 
    path('allproduct/',views.allproduct,name='allproduct'),
    path('proinfo/<int:pid>/',views.proinfo,name='proinfo'),
    path('category/<int:cid>/',views.products_by_category,name='products_by_category'),
    
    #CDUD for farmer 
    path('add_product/',views.add_product,name='add_product'),
    path('edit_product/<int:pid>/',views.pro_edit,name='pro_edit'),
    path('delete_delete/<int:pid>/',views.pro_delete,name='pro_delete'),

    #customer 
    path('customer/',views.customer_home,name='customer_home'),
    #review
    path('customer_review/',views.customer_review,name='customer_review')
]
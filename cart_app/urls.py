from django.urls import path
from . import views

urlpatterns = [
    path('', views.cart_home, name='cart_home'),
    path('addtocart/<int:pid>/', views.addtocart, name='addtocart'),
    path('update_cart/<int:item_id>/', views.update_cart, name='update_cart'),
    path('remove_from_cart/<int:item_id>/',views.remove_from_cart,name='remove_from_cart'),

    path('placer_order/',views.place_order,name='place_order'),
    path('payment/<int:order_id>/',views.payment_page,name='payment_page'),
    path('payment/process/<int:order_id>/',views.process_payment,name='process_payment'),
    path('payment/success/<int:order_id>/',views.payment_success,name='payment_success')

]

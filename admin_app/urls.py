from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/',views.admin_dashboard, name='admin_dashboard'),
    path('farmer_detail/<int:farmer_id>/',views.farmer_detail,name='farmer_detail'),
    path('farmer/accept/<int:farmer_id>/',views.accept_farmer,name='accept_farmer'),
    path('farmer/block/<int:farmer_id>/',views.block_farmer,name='block_farmer')
]

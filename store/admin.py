from django.contrib import admin
from . models import FarmerProfile,CustomerProfile,Category,Product
# Register your models here.
admin.site.register(FarmerProfile)
admin.site.register(CustomerProfile)
admin.site.register(Product)
admin.site.register(Category)

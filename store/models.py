from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class FarmerProfile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,null=True)
    name=models.CharField(max_length=30,null=True)
    phonenumber=models.CharField(max_length=10)
    address=models.TextField(null=True,blank=True)
    farm_name=models.CharField(null=True)
    is_verified=models.BooleanField(default=True)
    rating=models.FloatField(default=0)
    image=models.ImageField(upload_to='farmer_detail/',blank=True,null=True)
    rating=models.DecimalField(max_digits=3,decimal_places=2,default=0)
    rating_count=models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.name
    
class CustomerProfile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,null=True)
    name=models.CharField(max_length=30,null=True)
    phonenumber=models.CharField(max_length=10)
    address=models.TextField(null=True,blank=True)

    def __str__(self):
        return self.name

class Category(models.Model):
     name = models.CharField(max_length=100)
     image = models.ImageField(upload_to='category_images/', blank=True)
     
     def __str__(self):
        return self.name


class Product(models.Model):
    farmer = models.ForeignKey(FarmerProfile, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)

    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.FloatField()
    stock = models.PositiveIntegerField()
    image = models.ImageField(upload_to='product_images/')
    created_at = models.DateTimeField(auto_now_add=True)
    rating =models.DecimalField(max_digits=3,decimal_places=2,default=0)
    rating_count=models.PositiveIntegerField(default=0)
    
    def __str__(self):
        return self.name

class Review(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    rating=models.IntegerField(default=5)
    comment=models.TextField()
    created_at=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review by {self.user.username} - {self.comment[:20]}"
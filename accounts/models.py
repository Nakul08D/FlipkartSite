from django.db import models
from django.contrib.auth.models import  User


class Buyer(models.Model):
    user=models.OneToOneField(User, related_name="buyer", on_delete=models.CASCADE)
    cat=models.CharField(default="buyer", max_length=50)
    number=models.IntegerField()
    
    def __str__(self):
        return self.user.username

class Seller(models.Model):
    user=models.OneToOneField(User, on_delete=models.CASCADE)
    cat=models.CharField(default="seller", max_length=50)
    number=models.IntegerField()
    address=models.CharField(max_length=50)
    city=models.CharField(max_length=50)
    
    def __str__(self):
        return self.user.username
    
class Product_Category(models.Model):
    category=models.CharField(max_length=50)
    
    def __str__(self):
        return self.category
    
class Seller_Product(models.Model):
    product_category=models.ForeignKey(Product_Category, on_delete=models.CASCADE)
    seller=models.ForeignKey(Seller, on_delete=models.CASCADE)
    name=models.CharField(max_length=50)
    img=models.ImageField(upload_to='media/')
    price=models.IntegerField()
    description=models.CharField( max_length=550)
    quantity=models.IntegerField(default=2)
    
    def __str__(self):
        return self.name
    
class Cart(models.Model):
    buyer=models.ForeignKey(Buyer, on_delete=models.CASCADE,related_name="cart")
    seller_Product=models.ForeignKey(Seller_Product, on_delete=models.CASCADE)
    quantity=models.IntegerField(default=1)
    total_price=models.IntegerField(default=0)
    
    def __str__(self):
        return self.seller_Product.name
    
class Wallet(models.Model):
    user=models.OneToOneField(User, on_delete=models.CASCADE, related_name='wallet')
    fund=models.IntegerField()
    user_type=models.CharField( max_length=50,
    choices=
            [('seller',"Seller"),('buyer',"Buyer")]
            )
    
    def __str__(self):
        return self.user.username
    
class Buy_detail(models.Model):
    buyer=models.ForeignKey(Buyer,on_delete=models.CASCADE)
    name=models.CharField( max_length=50)
    email=models.EmailField(max_length=254)
    number=models.IntegerField()
    address=models.CharField(max_length=100)
    total_amount=models.IntegerField()
    order_id=models.CharField(max_length=100, null=True, blank=True)
    razorpay_payment_id=models.CharField(max_length=100, null=True, blank=True)
    is_paid=models.BooleanField(default=False)
    

    def __str__(self):
        return self.name
    
    

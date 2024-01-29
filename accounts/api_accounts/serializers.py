from accounts.models import *
from django.contrib.auth.models import User
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=['username','first_name','last_name','email']
        
class BuyerSerializer(serializers.ModelSerializer):
    user=UserSerializer()
    class Meta:
        model=Buyer
        fields='__all__'

class SellerSerializer(serializers.ModelSerializer):
    #user=UserSerializer()
    class Meta:
        model=Seller
        fields='__all__'
        
class ProductCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model=Product_Category
        fields='__all__'        
           
class SellerProductSerializer(serializers.ModelSerializer):
    product_category=ProductCategorySerializer()
    seller =SellerSerializer()
    class Meta:
        model=Seller_Product
        fields="__all__"
        
class CartSerializer(serializers.ModelSerializer):  
    buyer = BuyerSerializer()
    seller_Product=SellerProductSerializer()
    class Meta:
        model=Cart
        fields='__all__'
        
class WalletSerializer(serializers.ModelSerializer):
    user=UserSerializer()
    class Meta:
        model=Wallet
        fields='__all__'

class BuyDetailSerializer(serializers.ModelSerializer):
    buyer=BuyerSerializer()
    class Meta:
        model=Buy_detail
        fields='__all__'

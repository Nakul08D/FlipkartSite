from django.contrib import admin
from .models import Seller,Buyer,Seller_Product,Product_Category,Cart,Wallet,Buy_detail

# Register your models here.

admin.site.register(Seller)
admin.site.register(Buyer)
#admin.site.register(Seller_Product)

@admin.register(Seller_Product)
class SPA(admin.ModelAdmin):
    list_display=['name',"seller_id"]
    
admin.site.register(Product_Category)
admin.site.register(Cart)
admin.site.register(Wallet)
admin.site.register(Buy_detail)






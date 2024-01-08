
from django.shortcuts import render,redirect,HttpResponse
from django.contrib import messages
from django.contrib.auth.models import User
from accounts.models import Seller_Product,Seller,Buyer,Product_Category,Cart,Wallet,Buy_detail
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
import razorpay

# Create your views here.

def home(request):
    # if request.user.is_anonymous:
    #     return redirect('base.html')
    products=Seller_Product.objects.all()
    context={'products':products}
    return render(request,'home.html',context)

def s_login(request):
    if request.method=="POST":
        username=request.POST.get('username')
        password=request.POST.get('password')
        
        if not User.objects.filter(username = username).exists():
            return redirect('s_login')
            
        user = User.objects.get(username = username)
        
        if not Seller.objects.filter(user_id=user.id).exists():
            return redirect('s_login')
        
        seller=authenticate(username=username,password=password)
        
        if seller is not None:
            login(request,user)
            return redirect('s_product')
        else:
            return redirect('s_login')
         
    return render(request,'s_login.html')

def s_sign_in(request):
    return render(request,'s_sign.html')

def s_sign_info(request):
    if request.method=="POST":
        username=request.POST.get('username')
        fname=request.POST.get('fname')
        lname=request.POST.get('lname')
        email=request.POST.get('email')
        password1=request.POST.get('password1')
        password2=request.POST.get('password2')
        number=request.POST.get('number')
        address=request.POST.get('address')
        city=request.POST.get('city')
        
        if(password1==password2):
            user=User.objects.create_user(username=username,first_name=fname,last_name=lname,email=email,password=password1)
            user.save()
        
            seller=Seller.objects.create(user=user,number=number,address=address,city=city)
            seller.save()
        else:
            print("Password are not same..")
        
        return render(request,'s_login.html')
    

        
def b_login(request):
        if request.method=="POST":
            username=request.POST.get('username')
            password=request.POST.get('password')
            
            if not User.objects.filter(username = username).exists():
                messages.info(request,"You entered wrong credential Check again....")
                return redirect('b_login')
            
            user = User.objects.get(username = username)
             
            if not Buyer.objects.filter(user_id=user.id).exists():
                messages.info(request,"You entered wrong credential Check again....")
                return redirect('b_login')
            
            buyer=authenticate(username=username,password=password)
            if (buyer is not None):
                login(request,user)
                return redirect('/')
            else:
                messages.info(request,"You entered wrong credential Check again....")
                return redirect('b_login')
        
        return render(request,'b_login.html')
    
def b_logout(request):
    logout(request)
    return redirect('home.html')

def s_logout(request):
    logout(request)
    return redirect('home.html')


def b_sign_in(request):
    if request.method=="POST":
        username=request.POST.get('username')
        fname=request.POST.get('fname')
        lname=request.POST.get('lname')
        email=request.POST.get('email')
        number=request.POST.get('number')
        password1=request.POST.get('password1')
        password2=request.POST.get('password2')
        
       
        if(password1==password2):
            user=User.objects.create_user(username=username,first_name=fname,last_name=lname,email=email,password=password1)
            user.save()
            
            buyer=Buyer.objects.create(user=user,number=number)
            buyer.save()
                                         
            return render(request,'b_login.html')
        else:
            print("Password are not same..")
    return render(request,'b_sign.html')


def s_product(request):
    if request.method=='POST':
        name=request.POST.get('name')
        category=request.POST.get('category')
        img=request.FILES.get('img')
        price=request.POST.get('price')
        description=request.POST.get('description')
        
        cat=Product_Category.objects.get(category=category)
        seller=Seller.objects.get(user_id=request.user.id)
    
        product=Seller_Product.objects.create(seller=seller,name=name,product_category=cat,img=img,price=price,description=description)
        product.save()
        
    return render(request,'s_product.html')

def s_product_detail(request):
    
    seller=Seller.objects.get(user_id=request.user.id)
    product=Seller_Product.objects.filter(seller_id=seller.id)

    context={'st':product}
    
    return render(request,'s_product_detail.html',context)

def add_to_cart(request,id):
    
    buyer=Buyer.objects.get(user=request.user)
    product=Seller_Product.objects.get(id=id)
    product.quantity=product.quantity-1
    product.save()
    cart=Cart.objects.filter(buyer_id=buyer.id)
         
    if product.quantity<0:
        messages.info(request,"Product is out of Stock")
        return redirect('/')
    for i in cart:
        if(i.seller_Product.name==product.name):
            i.quantity=i.quantity+1
            i.save()
            return redirect('/')
        
    
    cart_item=Cart.objects.create(buyer=buyer,seller_Product=product,total_price=product.price)
    cart_item.save()
    
    return redirect('/')


def view_cart(request):
    
    buyer=Buyer.objects.get(user_id=request.user.id)
    # cart = Cart.objects.filter(buyer_id = buyer.id)
    cart =buyer.cart.all()
    total_quantity=0
    total_amount=[]
    for i in cart:
        i.total_price = i.quantity*i.seller_Product.price
        i.save()
        total_amount.append(i.total_price)
    
    total_product_price = sum(total_amount)
    for i in cart:
        total_quantity=total_quantity+i.quantity

    context={'cart':cart,'total_quantity':total_quantity,'total_product_price':total_product_price}
    
    
    return render(request,'cart_view.html',context)


# def cart_count(request):
    
#     buyer=request.user
#     total_item=Cart.objects.filter(buyer_id=buyer.id)
#     cart_count=0
#     if total_item:
#         for item in total_item:
#             cart_count=cart_count+item.quantity
#             print("=======",cart_count)
#     else:
#         return 0
    
    # return {"cart_count":cart_count}




def remove(request,id):
    cart=Cart.objects.get(id=id)
    cart.delete()
    
    buyer=Buyer.objects.get(user_id=request.user.id)
    cart =buyer.cart.all()
    context={'cart':cart}
    
    return render(request,'cart_view.html',context)
    

def wallet(request):
    user=request.user
    wallet=Wallet.objects.get(user_id=user.id)
    context={'wallet':wallet,'user':user}
    
    if(wallet.user_type=='buyer'):
        return render(request,'wallet.html',context)
    else:
        return render(request,'s_wallet.html',context)
        
def add_fund_wallet(request):
    # buyer=Buyer.objects.get(user_id=request.user.id)
    if request.method=='POST':
        amount=request.POST.get('amount')
        wallet=Wallet.objects.get(user_id=request.user.id)
        wallet.fund=int(wallet.fund)+int(amount)
        wallet.save()
        messages.info(request,'Your amount is added.')
        return render(request,'add_fund.html')
    return render(request,'add_fund.html')
    
def buy_detail(request):
    buyer=Buyer.objects.get(user_id=request.user.id)
    cart =buyer.cart.all()
    
    total_amount=[]
    for i in cart:
        i.total_price = i.quantity*i.seller_Product.price
        i.save()
        total_amount.append(i.total_price)
    
    total_product_price = sum(total_amount)
    return render(request,'order_detail.html',{'total_product_price':total_product_price})

@csrf_exempt 
def buy(request):
    
    buyer=Buyer.objects.get(user_id=request.user.id)
    cart=Cart.objects.filter(buyer_id=buyer.id)
    price=0
    
    for i in cart:
        price=price+i.total_price
    
    wallet=Wallet.objects.get(user_id=request.user.id)
    if (price>wallet.fund):
        messages.info(request, "You Don't have Sufficient amount Please add more fund...")
    
    elif request.method=="POST":
        name=request.POST.get('name')
        email=request.POST.get('email')
        number=request.POST.get('number')
        address=request.POST.get('address1')
        
        buyer=Buyer.objects.get(user_id=request.user.id)
        cart =buyer.cart.all()
    
        total_amount=[]
        for i in cart:
            i.total_price = i.quantity*i.seller_Product.price
            i.save()
        total_amount.append(i.total_price)
    
        total_product_price = sum(total_amount)*100
        
        client=razorpay.Client(auth=(settings.KEY, settings.SECRET))
        payment=client.order.create({'amount':total_product_price, 'currency':'INR', 'payment_capture':1})
       
        buy_detail=Buy_detail.objects.create(buyer=buyer,name=name,email=email,number=number,address=address,total_amount=total_product_price,order_id=payment['id'])
        
        buy_detail.save()
        
        wallet.fund=wallet.fund-price
        wallet.save()
    
        cart.delete()
        return render(request,"order_detail.html",{'payment':payment})

    return render(request,'cart_view.html',{'cart':cart})

def success(request):
    buyer=Buyer.objects.get(user_id=request.user.id)
    buy_detail=Buy_detail.objects.filter(buyer_id=buyer.id)[::-1]
    buy_detail[0].is_paid = True
    buy_detail[0].save()
    
    return render(request,'success.html')
    

def view_item(request,id):
    
    product=Seller_Product.objects.get(id=id)
    context={'product':product}
    
    return render(request,'view_item.html',context)

def add(request,id):
    cart=Cart.objects.get(id=id)
    cart.quantity=cart.quantity+1
   
    product = Seller_Product.objects.get(id=cart.seller_Product.id)
    if(product.quantity<1):
        messages.info(request, "Product is Out of Stock...")
    else:
        product.quantity=product.quantity-1
        product.save()
        cart.save()
        
    return redirect('view_cart')
    
def minus(request,id):
    cart=Cart.objects.get(id=id)
    cart.quantity=cart.quantity-1
    product = Seller_Product.objects.get(id=cart.seller_Product.id)
    product.quantity=product.quantity+1
    product.save()
    cart.save()
    
    return redirect('view_cart')
    
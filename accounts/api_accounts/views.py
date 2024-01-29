from accounts.models import *
from django.contrib.auth.models import User
from accounts.api_accounts.serializers import *
from rest_framework import serializers
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from django.contrib.auth import authenticate
from rest_framework.decorators import permission_classes,authentication_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.contrib.auth.hashers import make_password
from rest_framework_simplejwt.tokens import RefreshToken

def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


@authentication_classes([JWTAuthentication])  
@permission_classes([IsAuthenticated]) 
class UserDetail(APIView):
    def get(self,request):
        try:
            user=User.objects.all()
            serializer=UserSerializer(user,many=True)
            context={'status':True,'data':serializer.data }
            return Response(context)
        except:
            context={'success':False, 'status':status.HTTP_204_NO_CONTENT, 'data':serializer.errors}
            return Response(context)
            
class BuyerRegistration(APIView):
    def post(self, request):
        try:
            serializer = UserSerializer(data=request.data)
            
            if serializer.is_valid():
                user = serializer.save(password=make_password(request.data.get('password')))
                Buyer.objects.create(user=user, number=request.data.get('number'))
                context = {'status': True, "data":"Create Successfully...."}
                return Response(context)
            else:
                context = {'status': False, 'data': serializer.errors}
                return Response(context)

        except Exception as e:
            context = {'status': False, 'msg': str(e)}
            return Response(context)
    
class BuyerLogin(APIView):
    def post(self,request):
        try:
            data=request.data
            username=data.get('username')
            password=data.get('password')
            
            if not User.objects.filter(username=username).exists():
                return Response({"msg":"Not Exists.."})
            
            user=User.objects.get(username=username)

            if not Buyer.objects.filter(user_id=user.id).exists():
                return Response({"msg":"Buyer Not Exist.."})
            
            user = authenticate(username=username, password=password)
            if user is not None:
                token=get_tokens_for_user(user)
                context={
                    "success":True,
                    "status": status.HTTP_302_FOUND,
                    "token":token,
                    "msg":"logIn"
                }
                return Response(context)
            else:
                return Response({"msg":"Not_logeIn"})
        except:
            return Response({"msg":"Invalid Creaditionals"})

    
class SellerRegistration(APIView):
    def post(self,request):
        try:
            serializer = UserSerializer(data=request.data)
            
            if serializer.is_valid():
                user=serializer.save(password=make_password(request.data.get('password')))
                Seller.objects.create(user=user,number=request.data.get('number'),city=request.data.get('city'),address=request.data.get('address'))
                context = {'status': True, "data":"Create Successfully...."}
                return Response(context)
            else:
                context = {'status': False, 'data':serializer.errors}
                return Response(context)

        except Exception as e:
            context = {'status': False, 'msg': str(e)}
            return Response(context)
   
class SellerLogin(APIView):
    def post(self,request):
        data=request.data
        username=request.data.get('username')
        password=request.data.get('password')
        
        try:
            if not User.objects.filter(username=username).exists():
                return Response({"msg":"User Not Found.."})
            
            user=User.objects.get(username=username)
            
            if not Seller.objects.filter(user_id=user.id).exists():
                return Response({"msg":"Seller Not Found.."})
            
            user=authenticate(username=username, password=password)
            if user is not None:
                token=get_tokens_for_user(user)
                context={
                    "success":True,
                    "status": status.HTTP_302_FOUND,
                    "token":token,
                    "msg":"logIn"
                }
                return Response(context)
            else:
                return Response({"msg":"Not_logeIn"})
        except:
            return Response({"msg":"Invalid Creaditionals"})


@authentication_classes([JWTAuthentication])  
@permission_classes([IsAuthenticated])        
class ProductCategory(APIView):
    def get(self,request):
        try:
            product_category = Seller_Product.objects.all()
            serializer=SellerProductSerializer(product_category, many=True)
            return Response(serializer.data)
        except Exception as e:
            return Response({"msg":str(e)})
        
    def post(self,request):
        serializer=ProductCategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            context={"status":True, "msg":"ProductCategory added..", "serializer":serializer.data}
            return Response(context)
        else:
            return Response(serializer.errors)


@authentication_classes([JWTAuthentication])  
@permission_classes([IsAuthenticated])        
class SellerProduct(APIView):
    def get(self, request, pk):
        try:
            product=Seller_Product.objects.filter(seller_id=pk)
            if product.exists():
                serializer=SellerProductSerializer(product, many=True)
                context={"status":True, "data":serializer.data}
                return Response(context)
            else:
                context={"status":False, "data":"No Product"}
                return Response(context)
        except:
            context={"status":False, "data":serializer.errors}
            return Response(context)
        
    def post(self, request, pk):
        try:
            data=request.data
            seller=Seller.objects.get(pk=pk)
            category=Product_Category.objects.get(category=data.get('category'))
            
            product=Seller_Product.objects.create(seller=seller,product_category=category,name=data.get('name'), price=data.get('price'), description=data.get('description'), img=data.get('img'))
            product.save()
        
            return Response({"msg":"Product Added.."})  
        except Exception as e:
            context = {"Status": False, "data": str(e)}
            return Response(context)

@authentication_classes([JWTAuthentication])  
@permission_classes([IsAuthenticated])       
class BuyerCart(APIView):
    def get(self, request, pk):
        try:
            buyer=Buyer.objects.get(pk=pk)
            cart=Cart.objects.filter(buyer_id=buyer.id)
            serializer=CartSerializer(cart, many=True)
            context={"status":True, "data":serializer.data}
            return Response(context)
      
        except Exception as e:
                context={"status":False, "data":str(e)}
                return Response(context)
    

    def post(self, request, pk):
        try:
            data = request.data
            product = Seller_Product.objects.get(pk=pk)
            buyer = Buyer.objects.get(user=request.user)
           
            cart = Cart.objects.create(buyer=buyer, quantity=data.get('quantity'), total_price=product.price,seller_Product=product)
            product.quantity=product.quantity-int(data.get('quantity'))
            product.save()
            serializer = CartSerializer(cart)
            context = {"status": True, "data": serializer.data}
            return Response(context)

        except Exception as e:
            context = {"status": False, "data": str(e)}
            return Response(context)

@authentication_classes([JWTAuthentication])  
@permission_classes([IsAuthenticated])        
class WalletDetail(APIView):
    def get(self, request, pk):
        try:
            user=User.objects.get(pk=pk)
            wallet=Wallet.objects.get(user_id=user.id)
            serializer=WalletSerializer(wallet)
            context = {"status": True, "data": serializer.data}
            return Response(context)
        except Exception as e:
            context = {"status": False, "data": str(e)}
            return Response(context)
        
    def post(self, request, pk):
        try:
            data = request.data
            user = User.objects.get(pk=pk)
            wallet = Wallet.objects.get(user_id=user.id)
            wallet.fund = wallet.fund + int(data.get('fund'))
            wallet.save()
            
            context = {"status": True, "data":f"Total Fund:{wallet.fund}"}
            return Response(context)
            
        except Exception as e:
            context = {"status": False, "data": str(e)}
            return Response(context)


@authentication_classes([JWTAuthentication])  
@permission_classes([IsAuthenticated])        
class BuyerBuyDetalil(APIView):
    def post(self, request, pk):
        try:
            data=request.data
            print("============",data)
            buyer=Buyer.objects.get(pk=pk)
            
            detail=Buy_detail.objects.create(buyer=buyer,name=request.data.get('name'), email=request.data.get('email'), address=request.data.get('address'), number=request.data.get('number'), total_amount=request.data.get('total_amount'), is_paid=request.data.get('is_paid'))
            serializer=BuyDetailSerializer(detail)
            context={"Status":True, "data":serializer.data}
            return Response(context)
        except Exception as e:
            context = {"status": False, "data": str(e)}
            return Response(context)
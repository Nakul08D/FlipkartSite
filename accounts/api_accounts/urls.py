from django.urls import path
from accounts.api_accounts.views import *



urlpatterns = [
    path('userdetail/',UserDetail.as_view(),name='UserDetail'),
    path('buyerregistration/',BuyerRegistration.as_view(),name='UserDetail'),
    path('buyerlogin/',BuyerLogin.as_view(),name='BuyerLogin'),
    path('sellerregistration/',SellerRegistration.as_view(),name='SellerDetail'),
    path('sellerlogin/',SellerLogin.as_view(),name='SellerLogin'),
    path('productcategory/',ProductCategory.as_view(), name='ProductCategory'),
    path('sellerproduct/<int:pk>/',SellerProduct.as_view(), name='SellerProduct'),
    path('buyercart/<int:pk>/', BuyerCart.as_view(), name='BuyerCart'),
    path('walletdetail/<int:pk>/', WalletDetail.as_view(), name='WalletDetail'),
    path('buyerbuydetail/<int:pk>/',BuyerBuyDetalil.as_view(), name='BuyerBuyDetail')
    
]


from django.urls import path
from .import views

#for media Files
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('',views.home,name='home'),
    path('s_login/',views.s_login,name='s_login'),
    path('s_sign_in/',views.s_sign_in,name='s_sign'),
    path('s_sign_info/',views.s_sign_info,name='s_sign'),
    path('b_login/',views.b_login,name='b_login'),
    path('b_logout/',views.b_login,name='b_logout'),
    path('s_logout/',views.b_login,name='b_logout'),
    path('b_sign_in/',views.b_sign_in,name='sign_in'),
    path('s_product/',views.s_product,name='s_product'),
    path('s_product_detail/',views.s_product_detail,name='s_product_detail'),
    path('add_to_cart/<int:id>',views.add_to_cart,name='add_to_cart'),
    path('view_cart/',views.view_cart,name='view_cart'),
    path('remove/<int:id>/',views.remove,name='remove'),
    path('wallet/',views.wallet,name='wallet'),
    path('add_fund_wallet/',views.add_fund_wallet,name='add_fund'),
    path('buy_detail/',views.buy_detail,name='buy_detail'),
    path('buy/',views.buy,name='buy'),
    path('success/',views.success,name='success'),
    path('view_item/<int:id>/',views.view_item,name='buy'),
    path('add/<int:id>/',views.add,name='add'),
    path('minus/<int:id>/',views.minus,name='minus'),
    
      
]
if settings.DEBUG:
  urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
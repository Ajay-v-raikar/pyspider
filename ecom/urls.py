from django.urls import path
from . import views

urlpatterns = [
    path('',views.login,name='login'),
    path('login',views.login,name='login'),
    path('signup',views.signup,name='signup'),
    path('main',views.main,name='main'),
    path('homeapplience',views.homeapplience,name='homeapplience'),
    path('cart',views.cart,name='cart'),
    path('product/cart',views.cart,name='cart'),
    path('checkout',views.checkout,name='checkout'),
    path('product',views.product, name="product"),
    path('product/<int:var1>',views.product, name="product"),
    path('product/addcart',views.addcart, name="addcart"),
    path('product/checkout',views.checkout, name="checkout"),
    path('product/main',views.main,name='main'),
    path('product/homeapplience',views.homeapplience,name='homeapplience'),
    path('checkout',views.checkout, name="checkout"),
]


from django.urls import path
from . import views
from django.contrib.auth import views as auth_views


app_name = 'kitchen'

urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('menu/', views.menu, name='menu'),
    path('contact/', views.contact, name='contact'),
    path('login/', views.user_login, name='login'), 
    path('logout/', views.logout_view, name='logout'),
    path('add-dish/', views.add_dish, name='add_dish'),
    path('cart/', views.cart_view, name='cart'),
    path('register/', views.register, name='register'),
    path('add-to-cart/<int:dish_id>/', views.add_to_cart, name='add_to_cart'),
     path('update_cart/<int:dish_id>/<str:action>/', views.update_cart, name='update_cart'),
    path('remove-from-cart/', views.remove_from_cart, name='remove_from_cart'),
    path('cart/add/<int:dish_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/remove/<int:dish_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('payment/success/', views.payment_success, name='payment_success'),
    path('payment-done/', views.payment_done, name='payment_done'), 
    path('faqs/', views.faqs, name='faqs'), 
    path('terms-condition/', views.terms_conditon, name='terms_condition'), 
    path('privacy-policy/', views.privacy_policy, name='privacy_policy' ),

    path('password-reset/',
         auth_views.PasswordResetView.as_view(
             template_name='password_reset.html',
             email_template_name='password_reset_email.txt',
             subject_template_name='password_reset_subject.txt',
             success_url='/password-reset/done/'
         ),
         name='password_reset'),

    path('password-reset/done/',
         auth_views.PasswordResetDoneView.as_view(template_name='password_reset_done.html'),
         name='password_reset_done'),

    
    
]




from django.urls import path
from django.contrib.auth import views as auth_views
from .views import *

urlpatterns = [
    path('', home, name='home'),
    path('product/', product, name='product'),
    path('add_product/', addProduct, name='add_product'),
    path('add_tags/', addTags, name='add_tags'),
    path('customer_details/<int:pk>/', customer, name='customer'),
    path('create_order/<str:pk>', createOrder, name='create_order'),
    path('update_order/<str:pk>', updateOrder, name='update_order'),
    path('delete_order/<str:pk>', deleteOrder, name='delete_order'),
    path('login/', loginPage, name='login'),
    path('logout/', logOutUser, name='logout'),
    path('register/', register, name='register'),
    path('user_page/', userPage, name='user_page'),
    path('customer_settings/', customer_settings, name='customer_setting'),

    path('reset_password/', auth_views.PasswordResetView.as_view(template_name='accounts/password_reset.html'),
         name='reset_password'),
    path('reset_password_done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset_password_compete/', auth_views.PasswordResetCompleteView.as_view(template_name='accounts/password_reset_done.html'),
         name='password_reset_complete'),

    path('delete_product/<str:pk>', deleteProduct, name='delete_product'),
    path('delete_tag/<str:pk>', deleteTags, name='delete_tag'),
]


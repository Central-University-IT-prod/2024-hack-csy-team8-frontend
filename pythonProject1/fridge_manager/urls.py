"""
URL configuration for fridge_manager project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.shortcuts import redirect
from products import views
from django.contrib.auth import views as auth_views
from products import views as product_views
from products.views import create_shopping_list, leave_group, add_product_to_shopping_list, shopping_list_detail, delete_shopping_list, delete_product_from_shopping_list, update_product_quantity, group_detail, remove_member

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('register/', views.register, name='register'),  # URL для регистрации
    path('products/', views.product_list, name='product_list'),
    path('products/add/', views.add_product, name='add_product'),
    path('shopping-list/', views.shopping_list, name='shopping_list'),
    path('shopping-list/create/', create_shopping_list, name='create_shopping_list'),
    path('shopping-list/<int:shopping_list_id>/add-product/', add_product_to_shopping_list, name='add_product_to_shopping_list'),
    path('shopping-list/<int:shopping_list_id>/', shopping_list_detail, name='shopping_list_detail'),
    path('shopping-list/add/', views.add_shopping_list, name='add_shopping_list'),
    path('profile/', views.profile_view, name='profile_view'),
    path('products/delete/<int:product_id>/', product_views.delete_product, name='delete_product'),
    path('product/<int:product_id>/update/', update_product_quantity, name='update_product_quantity'),
    path('groups/', product_views.group_list, name='group_list'),
    path('groups/create/', product_views.create_group, name='create_group'),
    path('groups/<int:group_id>/add-member/', product_views.add_member, name='add_member'),
    path('groups/<int:group_id>/products/', product_views.product_list, name='group_product_list'),
    path('groups/<int:group_id>/products/add/', product_views.add_product, name='add_product_in_group'),  # Добавление продукта в группу
    path('groups/<int:group_id>/', group_detail, name='group_detail'),
    path('groups/<int:group_id>/remove-member/<int:user_id>/', remove_member, name='remove_member'),
    path('shopping-list/<int:shopping_list_id>/delete/', delete_shopping_list, name='delete_shopping_list'),
    path('shopping-list/<int:shopping_list_id>/delete-product/<int:product_id>/', delete_product_from_shopping_list, name='delete_product_from_shopping_list'),
    path('groups/<int:group_id>/leave/', leave_group, name='leave_group'),
    path('', lambda request: redirect('product_list', permanent=False))
]
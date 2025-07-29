from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register, name='register'),
    path('', views.inventory_list, name='home'),  # ← root URL now shows inventory list
    path('inventory/', views.inventory_list, name='inventory_list'),
    path('inventory/add/', views.inventory_create, name='inventory_add'),
    path('inventory/edit/<int:pk>/', views.inventory_update, name='inventory_edit'),
    path('inventory/delete/<int:pk>/', views.inventory_delete, name='inventory_delete'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('inventory/add/', views.add_inventory_item, name='add_inventory_item'),
]
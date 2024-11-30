# portfolio/urls.py

from django.urls import path
from . import views
from .views import dashboard,add_stock,remove_stock


# urlpatterns = [
#     path('get_real_time_data/', views.get_real_time_data, name='get_real_time_data'),
#     path('get_stock_history/<str:ticker>/', views.get_stock_history, name='get_stock_history'),
#     # other paths...
#      path('', views.dashboard, name='dashboard'),
#     path('add/', views.add_stock, name='add_stock'),
#     path('remove/<int:id>/', views.remove_stock, name='remove_stock'),
#     path('login/', views.custom_login_view, name='custom-login'), 
# ]


urlpatterns = [
    
    path('', views.dashboard, name='dashboard'),
    path('login/', views.custom_login_view, name='custom-login'),
    path('add/', views.add_stock, name='add_stock'),
    path('remove_stock/<int:stock_id>/', views.remove_stock, name='remove_stock'),  # Ensure views.remove_stock is used
    
    # path('get_stock_history/<str:ticker>/', views.get_stock_history, name='get-stock-history'), 
     path('get_real_time_stock_data/<str:ticker>/', views.get_real_time_stock_data, name='get_real_time_stock_data'),
    path('get_stock_history/<str:ticker>/', views.get_stock_history, name='get_stock_history'),
]



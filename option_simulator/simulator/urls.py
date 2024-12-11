from django.urls import path
from . import views

urlpatterns = [
    path('', views.option_simulator, name='option_simulator'),
    path('get_expiry_dates/', views.get_expiry_dates, name='get_expiry_dates'),  # AJAX URL for expiry dates
    path('get_strike_prices/', views.get_strike_prices, name='get_strike_prices'),  # Add this line
    path('get_option_data_for_chart/', views.get_option_data_for_chart, name='get_option_data_for_chart'),
    
]
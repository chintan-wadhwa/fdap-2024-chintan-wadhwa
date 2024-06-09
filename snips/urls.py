from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('api/chart', views.api_chart_data, name='chart_data'),
    path('chart/', views.chart_page, name='chart_page'),
    path('api/deribit/', views.deribit_data, name='deribit_data'),
]

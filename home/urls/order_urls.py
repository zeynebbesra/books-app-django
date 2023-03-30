from django.urls import path
from home.views import order_views as views


urlpatterns = [
   path('add/', views.addOrderItems, name='orders-add'),
   path('<str:pk>/', views.getOrderById, name='user-order')
]

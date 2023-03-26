from django.shortcuts import render

from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.decorators import api_view, permission_classes

from home.models import Product, Order, OrderItem, ShippingAddress
from home.serializers import ProductSerializer


from rest_framework import status
# Create your views here.


 
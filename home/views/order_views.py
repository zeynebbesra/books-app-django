from django.shortcuts import render

from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.decorators import api_view, permission_classes

from home.models import Product, Order, OrderItem, ShippingAddress
from home.serializers import ProductSerializer, OrderSerializer


from rest_framework import status
# Create your views here.


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def addOrderItems(request):
    user = request.user
    data = request.data

    orderItems = data['orderItems']
    
    if orderItems and len(orderItems) == 0:
        return Response({'detail' : 'No Order Items'}, status=status.HTTP_400_BAD_REQUEST)
    else:

        # (1) Create Order
        
        order = Order.objects.create(
            user = user,
            paymentMethod = data['paymentMethod'],
            shippingPrice = data['shippingPrice'],
            totalPrice = data['totalPrice'],
        )

        # (2) Create shipping adddress

        shipping = ShippingAddress.objects.create(
            order = order,
            address = data['shippingAddress']['address'],
            city = data['shippingAddress']['city'],
            postalCode = data['shippingAddress']['postalCode'],
            country = data['shippingAddress']['country'],
        )

        # (3) Create order items adn set order to orderItem relationship

        for i in orderItems:
            product = Product.objects.get(_id = i['product'])

            item = OrderItem.objects.create(
                product = product,
                order = order,
                name = product.name,  
                # name = i[name]
                qty = i['qty'],
                price = i['price'],
                image = product.image.url,
            )

            # (4) Update stock

            product.countInStock -=item.qty
            product.save()

        serializer = OrderSerializer(order, many=False)
        return Response(serializer.data)

        





 
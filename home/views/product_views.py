from django.shortcuts import render

from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.decorators import api_view, permission_classes

from home.models import Product
from home.serializers import ProductSerializer


from rest_framework import status
# Create your views here.


@api_view(['GET'])
def getProducts(request):
    products = Product.objects.all()
    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def getProduct(request, pk):
    product = Product.objects.get(_id=pk)
    serializer = ProductSerializer(product, many=False)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAdminUser])
def createProduct(request):
    user = request.user
    data=request.data
    product = Product.objects.create(
        user=user,
        name=data['name'],
        author=data['author'],
        translator='Sample Name',
        publisher='Sample Name',
        price=0,
        countInStock=0,
    )
    serializer = ProductSerializer(product, many=False)
    return Response(serializer.data)


@api_view(['PATCH'])
@permission_classes([IsAdminUser])
def updateProduct(request, pk):
    data=request.data
    product = Product.objects.get(_id=pk)
    serializer = ProductSerializer(product, data=data, partial = True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    
    return Response(serializer.errors)
    

@api_view(['DELETE'])
@permission_classes([IsAdminUser])
def deleteProduct(request,pk):
    product = Product.objects.get(_id=pk)
    product.delete()
    return Response('Product Deleted')


@api_view(['POST'])
def uploadImage(request):
    data = request.data

    product_id = data['product_id']
    product = Product.objects.get(_id=product_id)

    product.image = request.FILES.get('image')
    product.save()

    return Response('Image was uploaded')
    
    
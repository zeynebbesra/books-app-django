from django.shortcuts import render

from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.decorators import api_view, permission_classes

from home.models import Product, Review
from home.serializers import ProductSerializer
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from rest_framework import status
# Create your views here.


@api_view(['GET'])
def getProducts(request):
    query = request.query_params.get('keyword')
    if query == None:   
        query = ''
    else:
        query = query.lower()

    products = Product.objects.filter(
        name__icontains=query)

    page = request.query_params.get('page')
    paginator = Paginator(products, 3)

    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)

    #İsteğin sayfa parametresi (page) kontrol edilir ve istek sayfasına göre ürünler belirlenir. 
    #Eğer sayfa parametresi bir sayı değilse veya sayfa parametresi verilen sayfalar arasında değilse, ilk sayfa veya son sayfa kullanılır.

    if page == None:
        page = 1

    # import ipdb; ipdb.set_trace()
    page = int(page)
    
    serializer = ProductSerializer(products, many=True)
    return Response({'products': serializer.data, 'page': page, 'pages': paginator.num_pages})




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
@permission_classes([IsAdminUser])
def uploadImage(request):
    data = request.data

    product_id = data['product_id']
    product = Product.objects.get(_id=product_id)

    product.image = request.FILES.get('image')
    product.save()

    return Response('Image was uploaded')
    

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def createProductReview(request, pk):
    user = request.user
    product = Product.objects.get(_id=pk)
    data = request.data

    #1 - Review already exists
    alreadyExists = product.review_set.filter(user=user).exists()
    if alreadyExists:
        content = {'details':'Product already reviewed'}
        return Response(content, status=status.HTTP_409_CONFLICT)
    
    
    #2 - Create review
    else:
        review = Review.objects.create(
            user=user,
            product=product,
            name=user.first_name,
            comment=data['comment'],
        )

        reviews=product.review_set.all() #we're going to get all of the product review
        product.numReviews = len(reviews) #we find out how many reviews the product has
        product.save()

        return Response('Review Added')





from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static  # it allows us to connect our URL 

urlpatterns = [
    path('admin/', admin.site.urls),
    #path('api/', include('home.urls')),
    path('api/products/', include('home.urls.product_urls')),
    path('api/users', include('home.urls.user_urls')),
    path('api/orders', include('home.urls.order_urls')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
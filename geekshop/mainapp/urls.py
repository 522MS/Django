from django.urls import path
from .views import products, product
from django.views.decorators.cache import cache_page

app_name = 'products'

urlpatterns = [
    path('', products, name='index'),
    path('category/<int:pk>/', cache_page(3600)(products), name='category'),
    path('category/<int:pk>/page/<int:page>/', products, name='page'),
    path('product/<int:pk>/', product, name='product')
]
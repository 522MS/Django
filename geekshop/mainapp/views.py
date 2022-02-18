import random

from django.shortcuts import render, get_object_or_404

from basketapp.models import Basket
from mainapp.models import ProductCategory, Product

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from django.conf import settings
from django.core.cache import cache

from django.views.decorators.cache import cache_page
from django.views.decorators.cache import never_cache

from django.db import connection
from django.db.models.signals import pre_save
from django.dispatch import receiver


def get_links_menu():
    if settings.LOW_CACHE:
        key = 'links_menu'
        links_menu = cache.get(key)
        if links_menu is None:
            links_menu = ProductCategory.objects.filter(is_deleted=False)
            cache.set(key, links_menu)
        return links_menu
    else:
        return ProductCategory.objects.filter(is_deleted=False)


def get_category(pk):
    if settings.LOW_CACHE:
        key = f'category_{pk}'
        category = cache.get(key)
        if category is None:
            category = get_object_or_404(ProductCategory, pk=pk)
            cache.set(key, category)
        return category
    else:
        return get_object_or_404(ProductCategory, pk=pk)


def get_products():
    if settings.LOW_CACHE:
        key = 'products'
        products = cache.get(key)
        if products is None:
            products = Product.objects.filter(is_deleted=False)
            cache.set(key, products)
        return products
    else:
        return Product.objects.filter(is_deleted=False)


def get_product(pk):
    if settings.LOW_CACHE:
        key = f'product_{pk}'
        product = cache.get(key)
        if product is None:
            product = get_object_or_404(Product, pk=pk)
            cache.set(key, product)
        return product
    else:
        return get_object_or_404(Product, pk=pk)


def get_products_ordered_by_price():
    if settings.LOW_CACHE:
        key = 'products_ordered_by_price'
        products = cache.get(key)
        if products is None:
            products = Product.objects.filter(is_deleted=False, category__is_deleted=False).order_by('price')
            cache.set(key, products)
        return products
    else:
        return Product.objects.filter(is_deleted=False, category__is_deleted=False).order_by('price')


def get_products_in_category_ordered_by_price(pk):
    if settings.LOW_CACHE:
        key = f'products_in_category_ordered_by_price_{pk}'
        products = cache.get(key)
        if products is None:
            products = Product.objects.filter(category__pk=pk, is_deleted=False, category__is_deleted=False).order_by(
                'price')
            cache.set(key, products)
        return products
    else:
        return Product.objects.filter(category__pk=pk, is_deleted=False, category__is_deleted=False).order_by('price')


def get_hot_product():
    products = get_products()

    return random.sample(list(products), 1)[0]


def get_same_products(hot_product):
    same_products = Product.objects.filter(category=hot_product.category).exclude(pk=hot_product.pk)
    return same_products


@cache_page(3600)
def products(request, pk=None, page=1):
    title = 'продукты/каталог'

    links_menu = get_links_menu()
    hot_product = get_hot_product()
    same_products = get_same_products(hot_product)

    if pk is not None:
        if pk == 0:
            products = get_products_ordered_by_price()
            category = {'pk': 0, 'name': 'все'}
        else:
            category = get_category(pk)
            products = get_products_in_category_ordered_by_price(pk)

        paginator = Paginator(products, 2)

        try:
            products_paginator = paginator.page(page)
        except PageNotAnInteger:
            products_paginator = paginator.page(1)
        except EmptyPage:
            products_paginator = paginator.page(paginator.num_pages)

        context = {
            'title': title,
            'links_menu': links_menu,
            'products': products_paginator,
            'category': category,
            'hot_product': hot_product,
            'same_products': same_products,
        }
        return render(request=request, template_name='mainapp/products.html', context=context)

    context = {
        'title': title,
        'links_menu': links_menu,
        'hot_product': hot_product,
        'same_products': same_products,
    }
    return render(request=request, template_name='mainapp/products.html', context=context)


def product(request, pk):
    title = 'продукты'

    context = {
        'title': title,
        'links_menu': get_links_menu(),
        'product': get_product(pk),
    }

    return render(request, 'mainapp/product.html', context)


def db_profile_by_type(prefix, type, queries):
    update_queries = list(filter(lambda x: type in x['sql'], queries))
    print(f'db_profile {type} for {prefix}:')
    [print(query['sql']) for query in update_queries]


@receiver(pre_save, sender=ProductCategory)
def product_is_active_update_productcategory_save(sender, instance, **kwargs):
    if instance.pk:
        if instance.is_deleted:
            instance.product_set.update(is_deleted=True)
        else:
            instance.product_set.update(is_deleted=False)

        db_profile_by_type(sender, 'UPDATE', connection.queries)

from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse, reverse_lazy

from adminapp.forms import ShopUserAdminEditForm, ProductEditForm, CategoryEditForm
from authapp.forms import ShopUserRegisterForm
from authapp.models import ShopUser
from django.shortcuts import get_object_or_404, render
from mainapp.models import Product, ProductCategory
from django.contrib.auth.decorators import user_passes_test

from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView


class UsersListView(ListView):
    model = ShopUser
    template_name = 'adminapp/users.html'
    context_object_name = 'objects'
    paginate_by = 3

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(UsersListView, self).get_context_data()
        context['title'] = 'админка/пользователи'
        return context

    def get_queryset(self):
        return ShopUser.objects.all().order_by('is_deleted', '-is_superuser', '-is_staff', 'username')


class UserCreateView(CreateView):
    template_name = 'adminapp/user_create.html'
    form_class = ShopUserRegisterForm
    success_url = reverse_lazy('admin_staff:users')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(UserCreateView, self).get_context_data()
        context['title'] = 'пользователи/создать'
        return context


class UserUpdateView(UpdateView):
    model = ShopUser
    form_class = ShopUserAdminEditForm
    template_name = 'adminapp/user_update.html'
    success_url = reverse_lazy('admin_staff:users')

    def get_context_data(self, **kwargs):
        context = super(UserUpdateView, self).get_context_data()
        context['title'] = 'пользователи/редактировать'
        return context


class UserDeleteView(DeleteView):
    model = ShopUser
    template_name = 'adminapp/user_delete.html'
    success_url = reverse_lazy('admin_staff:users')

    def get_context_data(self, **kwargs):
        context = super(UserDeleteView, self).get_context_data()
        context['title'] = 'пользователи/удалить'
        return context

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.is_deleted = True
        self.object.is_active = False
        self.object.save()

        return HttpResponseRedirect(self.get_success_url())


class CategoriesListView(ListView):
    model = ProductCategory
    template_name = 'adminapp/categories.html'
    context_object_name = 'objects'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(CategoriesListView, self).get_context_data()
        context['title'] = 'админка/категории'
        return context


class CategoryCreateView(CreateView):
    template_name = 'adminapp/category_create.html'
    success_url = reverse_lazy('admin_staff:categories')
    form_class = CategoryEditForm

    def get_context_data(self, **kwargs):
        context = super(CategoryCreateView, self).get_context_data()
        context['title'] = 'категория/создать'
        return context


class CategoryUpdateView(UpdateView):
    model = ProductCategory
    template_name = 'adminapp/category_update.html'
    success_url = reverse_lazy('admin_staff:categories')
    form_class = CategoryEditForm

    def get_context_data(self, **kwargs):
        context = super(CategoryUpdateView, self).get_context_data()
        context['title'] = 'категории/редактировать'
        return context


class CategoryDeleteView(DeleteView):
    model = ProductCategory
    template_name = 'adminapp/category_delete.html'
    success_url = reverse_lazy('admin_staff:categories')

    def get_context_data(self, **kwargs):
        context = super(CategoryDeleteView, self).get_context_data()
        context['title'] = 'категории/удалить'
        return context

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.is_deleted = True
        self.object.save()

        return HttpResponseRedirect(self.get_success_url())


class ProductsListView(ListView):
    model = Product
    template_name = 'adminapp/products.html'
    context_object_name = 'objects'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ProductsListView, self).get_context_data()
        category = get_object_or_404(ProductCategory, pk=self.kwargs['pk'])
        context['category'] = category
        context['title'] = 'админка/продукт'
        return context

    def get_queryset(self):
        return Product.objects.filter(category__pk=self.kwargs['pk']).order_by('name')


class ProductCreateView(CreateView):
    template_name = 'adminapp/product_create.html'
    form_class = ProductEditForm

    def get_initial(self):
        category = get_object_or_404(ProductCategory, pk=self.kwargs['pk'])
        initial = {'category': category}
        return initial

    def get_success_url(self):
        success_url = reverse_lazy('admin_staff:products', args=[self.kwargs['pk']])
        return success_url

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ProductCreateView, self).get_context_data()
        context['title'] = 'продукты/создать'
        return context


class ProductDetailView(DetailView):
    model = Product
    template_name = 'adminapp/product_read.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ProductDetailView, self).get_context_data()
        context['title'] = 'продукты/подробнее'
        return context


class ProductUpdateView(UpdateView):
    model = Product
    template_name = 'adminapp/product_update.html'
    form_class = ProductEditForm

    def get_success_url(self):
        category_pk = Product.objects.filter(pk=self.kwargs['pk'])[0].category.pk
        success_url = reverse_lazy('admin_staff:products', args=[category_pk])
        return success_url

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ProductUpdateView, self).get_context_data()
        context['title'] = 'продукты/редактировать'
        return context


class ProductDeleteView(DeleteView):
    model = Product
    template_name = 'adminapp/product_delete.html'

    def get_success_url(self):
        category_pk = Product.objects.filter(pk=self.kwargs['pk'])[0].category.pk
        success_url = reverse_lazy('admin_staff:products', args=[category_pk])
        return success_url

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.is_deleted = True
        self.object.save()

        return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ProductDeleteView, self).get_context_data()
        context['title'] = 'продукт/удалить'
        return context

from django.shortcuts import render, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from products.models import Product, ProductCategory, Basket
from django.db.models import ObjectDoesNotExist


# Create your views here.


def index(request):
    context = {
        'title': 'Главная страница',
    }
    return render(request, 'products/index.html', context)


def products(request):
    context = {
        'title': 'Store - Каталог',
        'products': Product.objects.all(),
        'categories': ProductCategory.objects.all(),
    }
    return render(request, 'products/products.html', context)


@login_required
def basket_add(request, product_id):
    product = Product.objects.get(id=product_id)
    try:
        basket = Basket.objects.get(user=request.user, product=product)
        basket.quantity += 1
        basket.save()
    except ObjectDoesNotExist:
        Basket.objects.create(user=request.user, product=product, quantity=1)
    return HttpResponseRedirect(request.META["HTTP_REFERER"])


@login_required
def basket_remove(request, basket_id):
    basket = Basket.objects.get(id=basket_id)
    basket.delete()
    return HttpResponseRedirect(request.META["HTTP_REFERER"])

from django.shortcuts import render,get_object_or_404,redirect
from .models import Product

def home(request):
    products = Product.objects.all()
    return render(request, 'uzum.html', {'products': products})

def product_info(request, pk):
    product = get_object_or_404(Product, pk=pk)
    related_products = Product.objects.exclude(pk=pk)[:5]  # Пример: другие товары
    return render(request, 'product_info.html', {
        'product': product,
        'products': related_products,  # для product_cards.html
    })

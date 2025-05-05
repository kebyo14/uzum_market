from django.shortcuts import render,get_object_or_404,redirect
from .models import Product, Order
from django.contrib.auth import authenticate, login
from django.contrib import messages

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
def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate(request, username=email, password=password)

        if user is not None:
            login(request, user)
            return redirect('/admin') 
        else:
            messages.error(request, 'Неверный логин или пароль')
    
    return render(request, 'login.html')

from .models import Product, Category

def catalog(request):
    category_id = request.GET.get('category')
    categories = Category.objects.all()
    if category_id:
        products = Product.objects.filter(category_id=category_id)
    else:
        products = Product.objects.all()
    return render(request, 'catalog.html', {
        'products': products,
        'categories': categories,
        'selected_category': int(category_id) if category_id else None,
    })


def register_order(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        password = request.POST.get('password')

        if name and email and password:
            if Order.objects.filter(email=email).exists():
                return render(request, 'register.html', {'error': 'Этот email уже зарегистрирован'})

            order = Order(Name=name, email=email, password=password)
            order.save()

            request.session['user_name'] = name
            return redirect('home')  
        else:
            return render(request, 'register.html', {'error': 'Все поля должны быть заполнены'})

    return render(request, 'register.html')



def logout_view(request):
    request.session.flush() 
    return redirect('home')


def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            user = Order.objects.get(email=email, password=password)
            request.session['user_name'] = user.Name  # сохраняем имя
            return redirect('home')  # или куда нужно
        except Order.DoesNotExist:
            messages.error(request, 'Неверный логин или пароль')

    return render(request, 'login.html')

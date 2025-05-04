from django.shortcuts import render, redirect
from .models import Product
from django.contrib.auth import authenticate, login
from django.contrib import messages

def home(request):
    products = Product.objects.all()
    return render(request, 'uzum.html', {'products': products})


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
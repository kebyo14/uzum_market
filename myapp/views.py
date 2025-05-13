from django.shortcuts import render,get_object_or_404,redirect
from .models import Product,Comments,Contact2
from django.contrib.auth import authenticate, login
from django.contrib import messages
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


def link(request):
    user_img = request.session.get('user_img', None)
    comments = Comments.objects.all().order_by('-created_at')
    unread_count = Comments.objects.filter(is_read=False).count()  # Количество непрочитанных

    comments = Comments.objects.all()
    user_name = request.session.get('user_name', None)
    return render(request, 'admin/index3.html',{'user_name':user_name,'comments':comments,'comments': comments,
        'comments_unread_count': unread_count,'user_img': user_img})

def link_item(request):
    error_message = None

    if request.method == 'POST':
        name = request.POST.get('name')
        password = request.POST.get('password')

        user = Contact2.objects.filter(name=name, password=password).first()

        if user:
            request.session['user_name'] = user.name
            request.session['user_img'] = user.img.url if user.img else None  # Сохраняем изображение
            request.session.save()
            return redirect('index3')  # Перенаправление на index3.html
        else:
            error_message = "Неправильное имя или пароль"

    return render(request, 'admin/link_item.html', {'error_message': error_message})

# Create
def create_item(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        img = request.FILES.get('img')

        if password == confirm_password:
            Contact2.objects.create(name=name, email=email, password=password, img=img)
            return redirect('link_item')  # Перенаправление на логин-страницу

    return render(request, 'admin/create_item.html')


def update_item(request, item_id):
    item = get_object_or_404(Contact2, id=item_id)
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password1 = request.POST.get('confirm_password')
        img = request.FILES.get('img')
        item.name = name
        item.email = email
        item.password = password
        item.password1 = password1
        item.img = img
        item.save()
        return redirect('link_item')

    return render(request, 'admin/update_item.html', {'item': item})


def delete_item(request, item_id):
    item = get_object_or_404(Contact2, id=item_id)
    if request.method == 'POST':
        item.delete()
        return redirect('link_item')

    return render(request, 'admin/index3.html', {'item': item})

def mark_as_read(request, comment_id):
    """Функция для отметки сообщения как прочитанного"""
    comment = get_object_or_404(Comments, id=comment_id)
    comment.is_read = True
    comment.save()
    return redirect('index3') 


def comments_item(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        number = request.POST.get('number')
        email = request.POST.get('email')
        message = request.POST.get('message')
        if name and number and email and message:  # Bo‘sh maydonlarni tekshirish
            Comments.objects.create(name=name, number=number,email=email,message=message,is_read=False)
            return redirect('home')  # URL nomini to‘g‘ri qo‘ying
    return render(request,'comments.html')

def link(request):
    user_img = request.session.get('user_img', None)
    comments = Comments.objects.all().order_by('-created_at')
    unread_count = Comments.objects.filter(is_read=False).count()  # Количество непрочитанных

    comments = Comments.objects.all()
    user_name = request.session.get('user_name', None)
    return render(request, 'admin/index3.html',{'user_name':user_name,'comments':comments,'comments': comments,
        'comments_unread_count': unread_count,'user_img': user_img})

from django.shortcuts import render, redirect, get_object_or_404
from .models import Product, Comments, Category  # Предположим, категории в модели Category

def product_base(request):
    comments = Comments.objects.all().order_by('-created_at')
    unread_count = Comments.objects.filter(is_read=False).count()
    user_img = request.session.get('user_img')
    user_name = request.session.get('user_name')
    product = Product.objects.all()

    return render(request, 'admin/pages/tables/product_base.html', {
        'product': product,
        'user_name': user_name,
        'user_img': user_img,
        'comments': comments,
        'comments_unread_count': unread_count,
    })

def create_product_base(request):
    comments = Comments.objects.all().order_by('-created_at')
    unread_count = Comments.objects.filter(is_read=False).count()
    user_img = request.session.get('user_img')
    user_name = request.session.get('user_name')

    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        price = request.POST.get('price')
        image = request.FILES.get('image')  # Файлы должны извлекаться через FILES
        category_id = request.POST.get('category')

        if all([name, description, price, image, category_id]):
            category = get_object_or_404(Category, id=category_id)
            Product.objects.create(
                name=name,
                description=description,
                price=price,
                image=image,
                category=category
            )
            return redirect('index3')

    return render(request, 'admin/pages/tables/create_product_base.html', {
        'user_name': user_name,
        'user_img': user_img,
        'comments': comments,
        'comments_unread_count': unread_count,
    })

def update_product_base(request, item_id):
    comments = Comments.objects.all().order_by('-created_at')
    unread_count = Comments.objects.filter(is_read=False).count()
    user_img = request.session.get('user_img')
    user_name = request.session.get('user_name')
    item = get_object_or_404(Product, id=item_id)
    categories = Category.objects.all()

    if request.method == 'POST':
        item.name = request.POST.get('name')
        item.description = request.POST.get('description')
        item.price = request.POST.get('price')

        if 'image' in request.FILES:
            item.image = request.FILES['image']

        category_id = request.POST.get('category')
        if category_id:
            item.category = get_object_or_404(Category, id=category_id)

        item.save()
        return redirect('index3')

    return render(request, 'admin/pages/tables/update_product_base.html', {
        'item': item,
        'categories': categories,
        'selected_category': item.category.id if item.category else None,
        'user_name': user_name,
        'user_img': user_img,
        'comments': comments,
        'comments_unread_count': unread_count,
    })

def delete_product_base(request, item_id):
    item = get_object_or_404(Product, id=item_id)
    if request.method == 'POST':
        item.delete()
        return redirect('product_base')

    return render(request, 'admin/index3.html', {'item': item})


def logout_view(request):
    request.session.flush() 
    return redirect('home')


def account_view(request):
    if 'user_name' not in request.session:
        return redirect('login')

    user = Order.objects.filter(Name=request.session['user_name']).first()

    if not user:
        return redirect('login')

    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        password = request.POST.get('password')

        if name and email:
            user.Name = name
            user.email = email
            if password:
                user.password = password  
            user.save()
            request.session['user_name'] = name
            messages.success(request, 'Данные успешно обновлены')

    return render(request, 'account.html', {'user': user})


def favorites_view(request):
    return render(request, 'favorites.html')


from django.http import JsonResponse
import json

def get_products_by_ids(request):
    if request.method == "POST":
        data = json.loads(request.body)
        ids = data.get('ids', [])
        products = Product.objects.filter(pk__in=ids)
        result = [
            {
                'id': p.pk,
                'name': p.name,
                'description': p.description[:50] + '...',
                'price': p.price,
                'image': p.image.url
            } for p in products
        ]
        return JsonResponse({'products': result})
    

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


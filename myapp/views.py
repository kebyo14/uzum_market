from django.shortcuts import render,get_object_or_404,redirect
from .models import Product,Comments,Contact2,Category,CustomUser
from django.contrib.auth import logout,authenticate, login
from django.contrib import messages
from django.http import HttpResponse
from django.core.mail import send_mail
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import random
from django.contrib.auth.decorators import login_required
from django.core.cache import cache
from django.utils.timezone import now
from utils.sms import send_sms_code  # импорт твоей функции отправки
from django.core.cache import cache  # для проверки кода

# 📤 Отправка SMS-кода
def send_sms_view(request):
    phone = request.GET.get("phone")
    # Автоматически добавим "+" если пользователь не ввёл
    if phone.startswith("998"):
        phone = "+" + phone
    elif not phone.startswith("+"):
        return JsonResponse({"error": "Номер должен начинаться с +998"}, status=400)
    try:
        send_sms_code(phone)
        return JsonResponse({"success": "Код отправлен"})
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

# ✅ Проверка кода
def verify_sms_code(request):
    phone = request.GET.get("phone")
    code = request.GET.get("code")

    if phone.startswith("998"):
        phone = "+" + phone
    cached_code = cache.get(f"sms_code:{phone}")
    if cached_code == code:
        return JsonResponse({"success": "Код подтвержден"})
    else:
        return JsonResponse({"error": "Неверный или просроченный код"}, status=400)

def phone_sms(request):
    phone = request.session.get('verification_phone')

    if request.method == 'POST':
        input_code = request.POST.get('code')
        correct_code = cache.get(f'verify_code:{phone}')

        if not correct_code:
            return render(request, 'phone_sms.html', {
                'error': '⏰ Срок действия кода истёк. Пожалуйста, зарегистрируйтесь снова.',
                'code_expiry_timestamp': 0
            })

        if input_code == correct_code:
            password = request.session.get('password')
            name = request.session.get('name')

            if CustomUser.objects.filter(phone=phone).exists():
                return render(request, 'phone_sms.html', {
                    'error': '❌ Пользователь с таким номером уже зарегистрирован.',
                    'code_expiry_timestamp': 0
                })

            # создаём пользователя
            user = CustomUser.objects.create_user(phone=phone, password=password, name=name)

            # очищаем
            cache.delete(f'verify_code:{phone}')
            request.session.pop('verification_phone', None)
            request.session.pop('password', None)
            request.session.pop('name', None)

            return render(request, 'success.html')

        else:
            ttl = cache.ttl(f'verify_code:{phone}') or 0
            expiry_timestamp = int(now().timestamp() + ttl)
            return render(request, 'phone_sms.html', {
                'error': '❌ Неверный код. Попробуйте снова.',
                'code_expiry_timestamp': expiry_timestamp
            })

    ttl = cache.ttl(f'verify_code:{phone}') or 0
    expiry_timestamp = int(now().timestamp() + ttl)
    return render(request, 'phone_sms.html', {
        'code_expiry_timestamp': expiry_timestamp
    })

def generate_code():
    return str(random.randint(100000, 999999))


def send_verification_email(email, code):
    send_mail(
        'Your Verification Code',
        f'Your verification code is: {code}',
        'anvarovpcaloxon14@gmail.com',  # Replace with your actual gmail
        [email],
        fail_silently=False,
    )

def register(request):
    if request.method == 'POST':
        method = request.POST.get('confirmation_method')  # 'email' или 'sms'
        password = request.POST['password']  # получаем пароль
        name = request.POST.get('name')

        if method == 'email':
            email = request.POST['email']
            if CustomUser.objects.filter(email=email).exists():
                return render(request, 'register.html', {
                    'error': '❌ Этот email уже используется.'
                })
            code = generate_code()
            # Кешируем код с привязкой к email, на 2 минуты
            cache.set(f'verify_code:{email}', code, timeout=120)
            # Пароль и email всё ещё можно держать в сессии
            request.session['verification_email'] = email
            request.session['password'] = password
            request.session['name'] = name
            send_verification_email(email, code)
            return redirect('verify')

        elif method == 'sms':
            phone = request.POST['phone']
            if phone.startswith("998"):
                phone = "+" + phone
            elif not phone.startswith("+"):
                return render(request, 'register.html', {
                    'error': 'Номер должен начинаться с +998'
            })
            if CustomUser.objects.filter(phone=phone).exists():
                return render(request, 'register.html', {
                    'error': '❌ Этот номер уже зарегистрирован.'
                })
            code = generate_code()
            cache.set(f'verify_code:{phone}', code, timeout=120)
            request.session['verification_phone'] = phone
            request.session['password'] = password
            request.session['name'] = name
            send_sms_code(phone)
            return redirect('phone_sms')  # этот шаблон оформим ниже

    return render(request, 'email_code.html')

def verify(request):
    if request.method == 'POST':
        input_code = request.POST.get('code')
        email = request.session.get('verification_email')
        correct_code = cache.get(f'verify_code:{email}')

        if not correct_code:
            return render(request, 'verify.html', {
                'error': '⏰ Срок действия кода истёк. Пожалуйста, зарегистрируйтесь снова.',
                'code_expiry_timestamp': 0
            })

        if input_code == correct_code:
            password = request.session.get('password')

            # Повторная проверка на наличие пользователя
            if CustomUser.objects.filter(email=email).exists():
                return render(request, 'verify.html', {
                    'error': '❌ Пользователь с таким email уже зарегистрирован.',
                    'code_expiry_timestamp': 0
                })

            # Создаём пользователя
            user = CustomUser.objects.create_user(email=email, password=password)

            # Удаляем код из кэша
            cache.delete(f'verify_code:{email}')

            # Очистка сессии при необходимости:
            request.session.pop('verification_email', None)
            request.session.pop('password', None)

            return render(request, 'success.html')
        else:
            ttl = cache.ttl(f'verify_code:{email}') or 0
            expiry_timestamp = int(now().timestamp() + ttl)
            return render(request, 'verify.html', {
                'error': '❌ Неверный код. Попробуйте снова.',
                'code_expiry_timestamp': expiry_timestamp
            })

    # GET-запрос — показать шаблон и таймер
    email = request.session.get('verification_email')
    ttl = cache.ttl(f'verify_code:{email}') or 0
    expiry_timestamp = int(now().timestamp() + ttl)
    return render(request, 'verify.html', {
        'code_expiry_timestamp': expiry_timestamp
    })


def resend_sms_code(request):
    phone = request.session.get('verification_phone')
    if phone:
        code = generate_code()
        cache.set(f'verify_code:{phone}', code, timeout=120)
        send_sms_code(phone)  # заменили на правильную функцию
        messages.success(request, '✅ Код был отправлен повторно.')
    return redirect('phone_sms')

def home(request):
    products = Product.objects.all()
    return render(request, 'uzum.html', {'products': products})

def product_info(request, pk):
    product = get_object_or_404(Product, pk=pk)
    related_products = Product.objects.exclude(pk=pk)[:5]  
    return render(request, 'product_info.html', {
        'product': product,
        'products': related_products,  
    })
def login_view(request):
    error_message = None

    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            error_message = '❌ Неверный email или пароль'

    return render(request, 'account/login.html', {'error_message': error_message})
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
    unread_count = Comments.objects.filter(is_read=False).count()  

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
            request.session['user_img'] = user.img.url if user.img else None  
            request.session.save()
            return redirect('index3')  
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
            return redirect('link_item')  

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
        if name and number and email and message:  
            Comments.objects.create(name=name, number=number,email=email,message=message,is_read=False)
            return redirect('home')  
    return render(request,'comments.html')

def link(request):
    user_img = request.session.get('user_img', None)
    comments = Comments.objects.all().order_by('-created_at')
    unread_count = Comments.objects.filter(is_read=False).count()  

    comments = Comments.objects.all()
    user_name = request.session.get('user_name', None)
    return render(request, 'admin/index3.html',{'user_name':user_name,'comments':comments,'comments': comments,
        'comments_unread_count': unread_count,'user_img': user_img})

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
    categories = Category.objects.all()

    if request.method == 'POST':
        form_type = request.POST.get('form_type')  # ✅ правильное имя

        if form_type == 'new_category':
            new_category_name = request.POST.get('new_category_name')
            if new_category_name:
                Category.objects.create(name=new_category_name)
            return redirect('create_product_base')

        elif form_type == 'new_product':
            name = request.POST.get('name')
            description = request.POST.get('description')
            price = request.POST.get('price')
            image = request.FILES.get('image')
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
        'categories': categories
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
        return redirect('product_base')


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

@login_required
def account_view(request):
    user = request.user
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        password = request.POST.get('password')

        if name and email:
            user.email = email
            user.first_name = name  # Или user.name, если есть поле
            if password:
                user.set_password(password)
            user.save()
            messages.success(request, 'Данные успешно обновлены')

    return render(request, 'account.html', {'user': user})

def delete_account_view(request):
    if request.user.is_authenticated:
        request.user.delete()
        logout(request)
        messages.success(request, 'Аккаунт успешно удалён.')
    return redirect('login_view')


def favorites_view(request):
    return render(request, 'favorites.html')


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
            if CustomUser.objects.filter(email=email).exists():
                return render(request, 'register.html', {'error': 'Этот email уже зарегистрирован'})

            order = CustomUser(name=name, email=email, password=password)
            order.save()

            request.session['user_name'] = name
            return redirect('home')  
        else:
            return render(request, 'register.html', {'error': 'Все поля должны быть заполнены'})

    return render(request, 'register.html')    

def korzina(request):
    return render(request, 'korzina.html')

@csrf_exempt
def get_products_by_ids(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            ids = data.get('ids', [])
            products = Product.objects.filter(id__in=ids)

            product_list = []
            for product in products:
                product_list.append({
                    'id': product.id,
                    'name': product.name,
                    'price': product.price,
                    'description': product.description[:100],
                    'image': product.image.url if product.image else '/static/img/no-image.png',
                })

            return JsonResponse({'products': product_list})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

    return JsonResponse({'error': 'Invalid request method'}, status=405)

def checkout(request):
    return render(request,'checkout.html')
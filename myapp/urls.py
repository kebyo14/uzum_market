from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('product/<int:pk>/',views.product_info,name='product_info'),
    path('login/', views.login_view, name='login'),
    path('catalog/', views.catalog, name='catalog'),  # <-- имя catalog
    path('register/', views.register_order, name='register'), # <-- регистрация
    path('logout/', views.logout_view, name='logout'), # <-- выход из аккаунта
    path('account/', views.account_view, name='account'),
    path('favorites/', views.favorites_view, name='favorites'),
    path('api/get-products/', views.get_products_by_ids, name='get_products_by_ids'),
]

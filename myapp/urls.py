from django.urls import path,include
from . import views
from myapp import views

urlpatterns = [
    path('accounts/', include('allauth.urls')), 

    path("send-sms/", views.send_sms_view),
    path("verify-sms/", views.verify_sms_code),
    path("phone_sms/",views.phone_sms, name='phone_sms'),
    path('resend_sms/', views.resend_sms_code, name='resend_sms_code'),
    path('register/', views.register, name='register'),
    path('verify/', views.verify, name='verify'),
    path('', views.home, name='home'),
    path('product/<int:pk>/',views.product_info,name='product_info'),
    path('login/', views.login_view, name='login_view'),
    path('logout/', views.logout_view, name='logout'), # <-- выход из аккаунта
    path('account/', views.account_view, name='account'),
    path('korzina/', views.korzina, name='korzina'),
    path('get-products/', views.get_products_by_ids, name='get_products_by_ids'),
    path('checkout/', views.checkout, name='checkout'),
    path('favorites/', views.favorites_view, name='favorites'),
    path('api/get-products/', views.get_products_by_ids, name='get_products_by_ids'),
    path('delete-account/', views.delete_account_view, name='delete_account'),

    path('catalog/', views.catalog, name='catalog'),  # <-- имя catalog
    path('admin/',views.link_item,name='link_item'),
    path('register/', views.register_order, name='register'),
    path('admin/index3.html', views.link, name='index3'),
    path('admin/pages/product_base',views.product_base,name='product_base'),
    path('admin/tables/index3.html', views.link, name='index3_tables'),
    path('admin/create/',views.create_item, name='create_item'),
    path('admin/update/<int:item_id>/',views.update_item, name='update_item'),
    path('admin/delete/<int:item_id>/',views.delete_item, name='delete_item'),
    path('comments.html/',views.comments_item,name='comments_item'),
    path('mark_as_read/<int:comment_id>/', views.mark_as_read, name='mark_as_read'),
    path('admin/tables/product_base.html',views.product_base,name='product_base'),
    path('admin/tables/update_product_base/<int:item_id>/',views.update_product_base, name='update_product_base'),
    path('create_product_base/',views.create_product_base, name='create_product_base'),
    path('delete_product_base/<int:item_id>/', views.delete_product_base, name='delete_product_base'),
]

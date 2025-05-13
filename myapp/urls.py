from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('product/<int:pk>/',views.product_info,name='product_info'),
    path('login/', views.login_view, name='login'),
    path('catalog/', views.catalog, name='catalog'),  # <-- имя catalog
    path('admin/',views.link_item,name='link_item'),
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

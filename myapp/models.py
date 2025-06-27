from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from .managers import CustomUserManager

class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name="Категория")

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=255, verbose_name="Название")
    description = models.TextField(verbose_name="Описание")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена")
    image = models.ImageField(upload_to='products/', verbose_name="Изображение", blank=True, null=True)
    category = models.ForeignKey(
        'Category',
        on_delete=models.CASCADE,
        related_name='products',
        verbose_name="Категория",
        blank=True,
        null=True
    )

    def __str__(self):
        return self.name
    

class Polzovatel(models.Model):
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)

    def str(self):
        return self.email    

class Contact2(models.Model):
    name = models.CharField(max_length=100,null=False,blank=False)
    email = models.EmailField(max_length=255,null=False,blank=False)
    password = models.CharField(max_length=100,null=False, blank=False)
    confirm_password = models.CharField(max_length=100,null=False,blank=False)
    img = models.ImageField(upload_to='images/', blank=True, null=True)
    def __str__(self):
        return self.name

class Comments(models.Model):
    name = models.CharField(max_length=255,null=False,blank=False)
    number = models.CharField(max_length=30,null=False, blank=False)
    email = models.EmailField(max_length=255,null=False,blank=False)
    message = models.CharField(max_length=255,null=False,blank=False)
    created_at = models.TimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)  # Новое поле для отметки прочтения
    
    def __str__(self):
        return f"{self.name} - {'Прочитано' if self.is_read else 'Непрочитано'}"




class CustomUser(AbstractUser):
    username = None
    name = models.CharField(max_length=150, blank=True)
    email = models.EmailField(_("email address"), unique=True, null=True, blank=True)
    phone = models.CharField(max_length=20, unique=True, null=True, blank=True)  # добавлено
    email_active = models.BooleanField(default=False)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    # Не трогаем groups и user_permissions — они будут взяты из AbstractUser

    def __str__(self):
        return self.email
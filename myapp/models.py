from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=255, verbose_name="Название")
    description = models.TextField(verbose_name="Описание")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена")
    image = models.ImageField(upload_to='products/', verbose_name="Изображение")

    def __str__(self):
        return self.name
    

class CustomUser(models.Model):
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)

    def str(self):
        return self.email    
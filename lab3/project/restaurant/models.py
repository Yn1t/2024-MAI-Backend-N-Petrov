from django.db import models

# Create your models here.


class Customer(models.Model):
    login = models.CharField(max_length=128, primary_key=True)
    password = models.CharField(max_length=128)

    def __str__(self):
        return self.login


class Dish(models.Model):
    dish_id = models.AutoField(primary_key=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, null=True)
    type = models.CharField(max_length=128)
    name = models.CharField(max_length=128)
    weight = models.FloatField()
    for_menu = models.BooleanField(default=True)

    def __str__(self):
        return str(self.dish_id)


class Menu(models.Model):
    name = models.CharField(max_length=128, primary_key=True)
    type = models.CharField(max_length=128)
    dishes = models.ManyToManyField(Dish)

    def __str__(self):
        return str(self.menu_id)

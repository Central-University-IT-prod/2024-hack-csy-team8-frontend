from django.db import models
from django.contrib.auth.models import User
from datetime import date

class Group(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    participants = models.ManyToManyField(User, through='Membership', related_name='custom_groups')  # Переименовали

    def __str__(self):
        return self.name

class Membership(models.Model):
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('member', 'Member'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)

    def __str__(self):
        return f"{self.user.username} в группе {self.group.name} как {self.role}"

class Product(models.Model):
    name = models.CharField(max_length=255)
    expiration_date = models.DateField(null=True, blank=True)
    quantity = models.PositiveIntegerField(default=1)
    added_by = models.ForeignKey(User, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE, null=True, blank=True, related_name='products')  # Привязка к группе

    def __str__(self):
        return self.name

    def is_expired(self):
        if self.expiration_date:
            return date.today() > self.expiration_date
        return False

class ShoppingList(models.Model):
    name = models.CharField(max_length=255)
    products = models.ManyToManyField('Product', through='ShoppingListProduct')
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class ShoppingListItem(models.Model):
    shopping_list = models.ForeignKey(ShoppingList, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity}x {self.product.name}"

class ShoppingListProduct(models.Model):
    shopping_list = models.ForeignKey(ShoppingList, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    class Meta:
        unique_together = ('shopping_list', 'product')

    def __str__(self):
        return f"{self.product.name} ({self.quantity}) in {self.shopping_list.name}"
# Create your models here.

from django.contrib import admin
from .models import Product
from .models import ShoppingList
from .models import ShoppingListItem
admin.site.register(Product)
admin.site.register(ShoppingList)
admin.site.register(ShoppingListItem)
# Register your models here.

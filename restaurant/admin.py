from django.contrib import admin
from .models import Category,MenuItem,Cart,Order,OrderItem,Booking,Menu
# Register your models here.

admin.site.register(Category)
admin.site.register(MenuItem)
admin.site.register(Cart)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Menu)
admin.site.register(Booking)


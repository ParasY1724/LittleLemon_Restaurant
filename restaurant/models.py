from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
   slug = models.SlugField()
   title = models.CharField(max_length = 255 ,db_index = True)

   def __str__(self):
        return self.title

class MenuItem(models.Model):
    title = models.CharField(max_length=255, db_index=True)
    price = models.DecimalField(max_digits=6, decimal_places=2,db_index=True)
    featured = models.BooleanField(db_index=True)
    category = models.ForeignKey(Category, on_delete=models.PROTECT)

    def __str__(self):
        return self.title


class Cart(models.Model):
   user = models.ForeignKey(User, on_delete=models.CASCADE)
   menuitem = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
   quantity = models.SmallIntegerField()
   unit_price = models.DecimalField(max_digits=6, decimal_places=2)
   price = models.DecimalField(max_digits=6, decimal_places=2)

   class Meta:
      unique_together = ['user', 'menuitem']

   def __str__(self):
      return f'{self.user.username} ordered items'
   

class Order(models.Model):
   user = models.ForeignKey(User, on_delete=models.CASCADE)
   delivery_crew = models.ForeignKey(User,on_delete = models.CASCADE, related_name = 'delivery_crew',null = True)
   status = models.BooleanField(db_index=True, default=0)
   total = models.DecimalField(max_digits=6, decimal_places=2)
   date = models.DateTimeField(db_index=True)

   def __str__(self):
      return f'{self.user} order'
   

class OrderItem(models.Model):
    order = models.ForeignKey(Order,on_delete = models.CASCADE)
    menuitem = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    quantity = models.SmallIntegerField()
    unit_price = models.DecimalField(max_digits=6, decimal_places=2)
    price = models.DecimalField(max_digits=6, decimal_places=2)

    class Meta:
      unique_together = ['order', 'menuitem']



class Booking(models.Model):
    first_name = models.CharField(max_length=200)
    reservation_date = models.DateField(null = True)
    reservation_slot = models.SmallIntegerField(default=10)

    def __str__(self): 
        return self.first_name



class Menu(models.Model):
   name = models.CharField(max_length = 200)
   price = models.IntegerField()
   menu_item_description = models.TextField(max_length=1000,default='')

   def __str__(self):
      return self.name
from rest_framework import serializers
from .models import Category,MenuItem,Cart,Order,OrderItem,Booking,Menu
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta():
        model = User
        fields = ['username']

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['slug','title']

class MenuItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = MenuItem
        fields = ['title','price','featured','category']

class UserListSerializer(serializers.ModelSerializer) :
    id = serializers.IntegerField(read_only = True)
    class Meta:
        model = User
        fields = ['id','username','email']

class CartSerializer(serializers.ModelSerializer):
    user = serializers.IntegerField(write_only = True)
    id = serializers.IntegerField(write_only = True)
    class Meta:
        model = Cart
        fields = '__all__'
class OrderItemSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(write_only = True)
    class Meta:
        model = OrderItem
        fields = '__all__'
    
class OrderSerializer(serializers.ModelSerializer):
    user = serializers.IntegerField(write_only = True)
    class Meta:
        model = Order
        fields = '__all__'


class OrderInsertSerializer(serializers.ModelSerializer):
    class Meta():
        model = Order
        fields = ['delivery_crew']
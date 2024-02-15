from rest_framework import serializers
from .models import Category,MenuItem,Cart,Order,OrderItem,Booking,Menu
from django.contrib.auth.models import User

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
# from django.http import HttpResponse
from django.shortcuts import render
from .forms import BookingForm
from django.contrib.auth.models import Group, User
from .models import Category,MenuItem,Cart,Order,OrderItem,Booking,Menu
from .serializers import MenuItemSerializer,UserListSerializer
from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated,IsAdminUser
from .permissions import IsManager, IsDeliveryCrew 
from rest_framework.response import Response
from rest_framework import status

class MenuItemsView(generics.ListAPIView) :
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer
    permission_classes = [IsAuthenticated]

class SingleMenuItemsView(generics.RetrieveUpdateDestroyAPIView):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer
    def get_permissions(self):
        if self.request.method == 'GET' :
            permission_classes = [IsAuthenticated]
        else :
            permission_classes = [IsManager]
        return[permission() for permission in permission_classes]

class ManagerView(generics.ListCreateAPIView) :
    queryset = User.objects.filter(groups__name='Manager')
    serializer_class = UserListSerializer
    permission_classes = [IsAdminUser | IsManager]

    def post(self,request):
        username = request.data['username']
        if username:
            user = get_object_or_404(User, username=username)
            manager = Group.objects.get(name = 'Manager')
            manager.user_set.add(user)
            return Response({'message':'User added to Managers'}, status.HTTP_201_CREATED)

class ManagerDestroyView(generics.DestroyAPIView):
    queryset = User.objects.filter(groups__name = 'Manager')
    serializer_class = UserListSerializer
    permission_classes = [IsAdminUser | IsManager]

    def delete(self,request,*args, **kwargs):
        pk = self.kwargs['pk']
        user = get_object_or_404(User, pk=pk)
        managers = Group.objects.get(name='Manager')
        managers.user_set.remove(user)
        return Response({'message':'User removed Managers'}, status.HTTP_200_OK)

class DeliveryCrewView(generics.ListCreateAPIView):
    queryset = User.objects.filter(groups__name = 'Delivery crew')
    serializer_class = UserListSerializer
    permission_classes = [IsAdminUser | IsManager]

    def post(self,request):
        username = request.data['username']
        if username:
            user = get_object_or_404(User, username=username)
            manager = Group.objects.get(name = 'Delivery crew')
            manager.user_set.add(user)
            return Response({'message':'User added to Managers'}, status.HTTP_201_CREATED)
        
class DeliveryDestroyView(generics.DestroyAPIView):
    queryset = User.objects.filter(groups__name = 'Delivery crew')
    serializer_class = UserListSerializer
    permission_classes = [IsAdminUser | IsManager]

    def delete(self,request,*args, **kwargs):
        pk = self.kwargs['pk']
        user = get_object_or_404(User, pk=pk)
        managers = Group.objects.get(name='Delivery crew')
        managers.user_set.remove(user)
        return Response({'message':'User removed Managers'}, status.HTTP_200_OK)   



def home(request):
    return render(request, 'index.html')

def about(request):
    return render(request, 'about.html')

def book(request):
    form = BookingForm()
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            form.save()
    context = {'form':form}
    return render(request, 'book.html', context)

# odd views
def menu(request):
    menu_data = Menu.objects.all()
    main_data = { "menu" :menu_data}
    return render(request,'menu.html',main_data)

def display_menu_items(request,pk = None):
    if pk :
        menu_item = Menu.objects.get(pk=pk)
    else:
        menu_item = ""

    return render(request,'menu_item.html',{"menu_item" : menu_item})
    
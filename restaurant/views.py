# from django.http import HttpResponse
from django.shortcuts import render
from .forms import BookingForm
from django.contrib.auth.models import Group, User
from .models import Category,MenuItem,Cart,Order,OrderItem,Booking,Menu
from .serializers import MenuItemSerializer,UserListSerializer,CartSerializer
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



class CartViewer(generics.ListCreateAPIView or  generics.DestroyAPIView):
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        try:
            return Cart.objects.filter(user=user)
        except Cart.DoesNotExist:
            return Cart.objects.none()
        
    def post(self, request, *args, **kwargs):
        id = request.data['menuitem']
        quantity = request.data['quantity']
        item = get_object_or_404(MenuItem,id=id)
        price = int(quantity) * item.price
        try:
            Cart.objects.create(user=request.user, quantity=quantity, unit_price=item.price, price=price, menuitem_id=id)
        except:
            return Response({'message':'Item already in cart'}, status.HTTP_409_CONFLICT)
        return Response({'message':'Item added to cart!'}, status.HTTP_201_CREATED)
    
    def delete(self, request, *args, **kwargs):
        Cart.objects.filter(user=request.user).delete()
        return Response({'message':'All Items removed from cart'}, status.HTTP_200_OK)

class Orderviwer(generics.RetrieveDestroyAPIView or generics.ListAPIView):
    pass

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
    
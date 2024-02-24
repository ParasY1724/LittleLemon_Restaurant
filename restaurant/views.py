# from django.http import HttpResponse
from django.shortcuts import render
from .forms import BookingForm
from django.contrib.auth.models import Group, User
from .models import Category,MenuItem,Cart,Order,OrderItem,Booking,Menu
from .serializers import MenuItemSerializer,UserListSerializer,CartSerializer,OrderItemSerializer,OrderSerializer,OrderInsertSerializer
from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle
from rest_framework.permissions import IsAuthenticated,IsAdminUser
from .permissions import IsManager, IsDeliveryCrew 
from rest_framework.response import Response
from rest_framework import status
from datetime import date
from django.core.paginator import Paginator,EmptyPage

class MenuItemsView(generics.ListAPIView) :
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer
    throttle_classes = [AnonRateThrottle, UserRateThrottle]
    permission_classes = []

    def get(self, request, *args, **kwargs):
        items = self.queryset
        search = request.query_params.get('search')
        ordering = request.query_params.get('ordering')
        page = request.query_params.get('page',default = 1)
        if search :
            items = items.filter(category__title=search).union(items.filter(title__icontains=search))
        if ordering :
            items = items.order_by(ordering)

        paginator = Paginator(items,per_page = 2)
        try :
            items = paginator.page(number=page)
        except EmptyPage :
            items = []
        serialized_item = MenuItemSerializer(items,many=True)
        return Response(serialized_item.data)
        

class SingleMenuItemsView(generics.RetrieveUpdateDestroyAPIView):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer
    throttle_classes = [AnonRateThrottle, UserRateThrottle]

    def get_permissions(self):
        if self.request.method == 'GET' :
            permission_classes = []
        else :
            permission_classes = [IsManager | IsAdminUser]
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
    throttle_classes = [AnonRateThrottle, UserRateThrottle]


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

class Orderviewer( generics.ListCreateAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]
    throttle_classes = [AnonRateThrottle, UserRateThrottle]

    def get_queryset(self):
        user = self.request.user
        if IsManager().has_permission(self.request, self) or IsAdminUser().has_permission(self.request, self):
            return Order.objects.all()
        elif IsDeliveryCrew().has_permission(self.request, self):
            return Order.objects.filter(delivery_crew=user)
        else:
            return Order.objects.filter(user=user)
        
    def post(self, request, *args, **kwargs):
        try:
            cart_list = Cart.objects.filter(user=request.user)
            total = 0
            order = Order.objects.create(user=request.user, status=False, total=0, date=date.today())
            for i in cart_list :
                total += i.price
                OrderItem.objects.create(order=order, quantity=i.quantity, unit_price=i.unit_price, price=i.price, menuitem= i.menuitem)
            # order.total = total
            # order.save()
            cart_list.delete()
        except Cart.DoesNotExist :
            return Response({'message':'cart is empty'},status.HTTP_200_OK)
    
        return Response({'message' : 'ordered successfull'},status.HTTP_200_OK)

class OrderSingleItemViewer(generics.ListAPIView):
    throttle_classes = [AnonRateThrottle, UserRateThrottle]


    def get_serializer_class(self):
        if self.request.method == 'GET' :
            return OrderItemSerializer
        else :
            return OrderSerializer  

    def get_permissions(self):
        user = self.request.user
        method = self.request.method
        order = Order.objects.filter(pk=self.kwargs['pk']).first()
        if order and user == order.user and method == 'GET':
            permission_classes = [IsAuthenticated]
        elif method == 'PUT' or method == 'DELETE':
            permission_classes = [IsManager | IsAdminUser]
        else :
            permission_classes = [IsDeliveryCrew | IsManager | IsAdminUser]
        return[permission() for permission in permission_classes] 
        
    def get_queryset(self, *args, **kwargs):
        query = OrderItem.objects.filter(order_id=self.kwargs['pk'])
        return query
    
    def delete(self, request, *args, **kwargs):
        order = Order.objects.get(pk=self.kwargs['pk'])
        order_number = str(order.id)
        order.delete()
        return Response({'message':f'Order #{order_number} was deleted'}, status.HTTP_200_OK)
    
    def patch(self, request, *args, **kwargs):
        try:
            order = Order.objects.get(pk=self.kwargs['pk'])
        except Order.DoesNotExist:
            return Response({'error': 'Order does not exist.'}, status=status.HTTP_404_NOT_FOUND)

        order.status = not order.status
        order.save()
        return Response({'message': 'Status of order #' + str(order.id) + ' changed to ' + str(order.status)}, status=status.HTTP_200_OK)

    def put(self, request, *args, **kwargs):
        serialized_item = OrderInsertSerializer(data=request.data)
        serialized_item.is_valid(raise_exception=True)
        order_pk = self.kwargs['pk']
        crew_pk = request.data['delivery_crew'] 
        order = get_object_or_404(Order, pk=order_pk)
        crew = get_object_or_404(User, pk=crew_pk)
        order.delivery_crew = crew
        order.save()
        return Response({'message':str(crew.username)+' was assigned to order #'+str(order.id)}, status.HTTP_201_CREATED)


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
    
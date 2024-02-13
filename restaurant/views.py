# from django.http import HttpResponse
from django.shortcuts import render
from .forms import BookingForm
from .models import Category,MenuItem,Cart,Order,OrderItem,Booking,Menu
from .serializers import MenuItemSerializer
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated,IsAdminUser
from .permissions import IsManager, IsDeliveryCrew 

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

        


# Create your views here.
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
    
from django.urls import path
from . import views


urlpatterns = [
    path('menu-items/',views.MenuItemsView.as_view(),name="Menu_Item"),
    path('menu-items/<int:pk>/',views.SingleMenuItemsView.as_view(),name="Menu_Item2"),
    path('groups/manager/users/',views.ManagerView.as_view(),name="Manager_View"),
    path('groups/manager/users/<int:pk>/',views.ManagerDestroyView.as_view(),name="Manager_killer"),
    path('groups/delivery-crew/users',views.DeliveryCrewView.as_view(),name="Delivey_view"),
    path('groups/delivery-crew/users/<int:pk>/',views.DeliveryDestroyView.as_view(),name="Delivey_view"),
    path('cart/menu-items',views.CartViewer.as_view(),name="Cart_View"),
    path('cart/orders',views.Orderviewer.as_view(),name="Order_view"),
    path('cart/orders/<int:pk>/',views.OrderSingleItemViewer.as_view(),name="OrderItem_view"),
    path('home/', views.home, name="home"),
    path('about/', views.about, name="about"),
    path('book/', views.book, name="book"),
    path('menu/',views.menu,name="menu"),
    path('menu_item/<int:pk>/', views.display_menu_items, name="menu_item"),
]
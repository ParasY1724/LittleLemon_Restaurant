from django.urls import path
from . import views


urlpatterns = [
    path('menu-items/',views.MenuItemsView.as_view(),name="Menu_Item"),
    path('menu-items/<int:pk>/',views.SingleMenuItemsView.as_view(),name="Menu_Item2"),
    path('', views.home, name="home"),
    path('about/', views.about, name="about"),
    path('book/', views.book, name="book"),
    path('menu/',views.menu,name="menu"),
    path('menu_item/<int:pk>/', views.display_menu_items, name="menu_item"),
]
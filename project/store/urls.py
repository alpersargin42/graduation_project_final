from django.urls import path,include
from . import views

urlpatterns = [
    path('',views.home,name='home'),
    path('about/',views.about,name='about'),
    path('login/',views.login_user,name='login'),
    path('logout/',views.logout_user,name='logout'),
    path('register/',views.register_user,name='register'),
    path('update_user/',views.update_user,name='update_user'),
    path('update_info/',views.update_info,name='update_info'),
    path('update_password/',views.update_password,name='update_password'),
    path('product/<int:pk>',views.product,name='product'),
    path('category/<str:foo>', views.category, name='category'),
    path('category_summary/', views.category_summary, name='category_summary'),
    path('search/',views.search,name='search'),
    path('product/add/', views.add_product, name='add_product'),
    path('product/<int:pk>/edit/', views.edit_product, name='edit_product'),
    path('product/<int:pk>/delete/', views.delete_product, name='delete_product'),
    path('product/process/', views.product_process, name='product_process'),
    path('product/list/', views.product_list, name='product_list'),
    path('send_message/<int:product_id>/', views.send_message, name='send_message'),
    path('inbox/', views.inbox, name='inbox'),
    path('sent_messages/', views.sent_messages, name='sent_messages'),
]

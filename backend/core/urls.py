from django.urls import path
from django.contrib.auth import views
from core.views import frontpage, signup, myaccount, edit_myaccount, contact, updateOrder
from product.views import product

urlpatterns = [
    path('', frontpage, name='frontpage'),
    path('contact/', contact, name='contact'),
    path('signup/', signup, name='signup'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('login/', views.LoginView.as_view(template_name='core/login.html'), name='login'),
    path('myaccount/', myaccount, name='myaccount'),
    path('myaccount/edit/', edit_myaccount, name='edit_myaccount'),
    path('update_order/<str:pk>/', updateOrder, name="updateOrder"),
    path('product/<slug:slug>/', product, name='product'),
    # path('shop/<slug:slug>/', product, name='product'),
] 
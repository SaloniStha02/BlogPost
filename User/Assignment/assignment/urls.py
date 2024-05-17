from django.urls import path
from .views import UserListView,UserDetailView,UserLogin
from rest_framework_simplejwt import views as jwt_views

urlpatterns =[
    path('users/', UserListView.user_list, name='user_list'),
    path('user-detail/<int:pk>/', UserDetailView.user_detail, name='user_detail'),
    path('login/', UserLogin.login, name='user_login'),
]
from django.urls import path
from .views import BlogView,BlogViewDetail,BlogHardDeleteView,BlogRestoreView

urlpatterns =[
    path('blogposts/', BlogView.blog_list, name='blog_list'),
    path('blogpost-detail/<int:pk>/', BlogViewDetail.blog_details, name='blog_details'),
    path('blogposts/<int:pk>/restore/', BlogRestoreView.blog_restore, name='blog_restore'),
    path('blogposts/<int:pk>/hard-delete/', BlogHardDeleteView.blog_hard_delete, name='blog_hard_delete'),

]
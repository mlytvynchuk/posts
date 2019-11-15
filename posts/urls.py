from django.urls import path
from .views import *
urlpatterns = [
    path('', PostListView.as_view(),name='post-home'),
    path('post/<int:pk>', post_detail, name='post-detail'),
    path('post/new/', PostCreateView.as_view(), name='post-create'),
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post-update'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),
    path('myposts/', user_posts, name='user-posts')
]
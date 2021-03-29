from django.urls import path
from django.contrib.auth.views import LoginView
from .views import PostsView, LogoutView, RegisterView, PostCreateView, PostDetailView


urlpatterns = [
    path('', PostsView.as_view(), name='home'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
    path('create/', PostCreateView.as_view(), name='create'),
    path('<slug:slug>/', PostDetailView.as_view(), name='detail'),
]

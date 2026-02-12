from django.urls import path
from django.contrib.auth.views import LogoutView
from . import views

urlpatterns = [
    path('signup/', views.SignUpView.as_view(), name='signup'),
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('setup/', views.GroupSetupView.as_view(), name='setup_group'),
    path('setup/create/', views.CreateGroupView.as_view(), name='create_group'),
    path('setup/join/', views.JoinGroupView.as_view(), name='join_group'),
    path('', views.DashboardView.as_view(), name='dashboard'),
]

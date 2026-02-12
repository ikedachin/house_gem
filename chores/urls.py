from django.urls import path
from . import views

urlpatterns = [
    path('', views.ChoreListView.as_view(), name='chore_list'),
    path('new/', views.ChoreCreateView.as_view(), name='chore_create'),

    path('<int:pk>/edit/', views.ChoreUpdateView.as_view(), name='chore_update'),
    path('<int:pk>/delete/', views.ChoreDeleteView.as_view(), name='chore_delete'),
    path('<int:pk>/complete/', views.ChoreCompleteView.as_view(), name='chore_complete'),
]

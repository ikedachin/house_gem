from django.urls import path
from . import views


urlpatterns = [
    path('ranking/', views.RankingView.as_view(), name='ranking'),
    path('analysis/', views.AnalysisView.as_view(), name='analysis'),
]

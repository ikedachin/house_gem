from django.views.generic import ListView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Sum, Count
from django.utils import timezone
from datetime import timedelta
from chores.models import ChoreExecution
from .models import WeeklyScore

class RankingView(LoginRequiredMixin, ListView):
    model = WeeklyScore
    template_name = 'gamification/ranking.html'
    context_object_name = 'scores'

    def get_queryset(self):
        if not self.request.user.house_group:
            return WeeklyScore.objects.none()
            
        today = timezone.now().date()
        year, week_num, _ = today.isocalendar()
        
        return WeeklyScore.objects.filter(
            group=self.request.user.house_group,
            year=year,
            week_number=week_num
        ).order_by('-total_points')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        today = timezone.now().date()
        year, week_num, _ = today.isocalendar()
        context['year'] = year
        context['week_number'] = week_num
        return context

class AnalysisView(LoginRequiredMixin, TemplateView):
    template_name = 'gamification/analysis.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        group = self.request.user.house_group
        if not group:
            return context

        # 1. ユーザー別貢献度 (円グラフ用) - 直近30日
        last_30_days = timezone.now() - timedelta(days=30)
        
        # 集計: ユーザーごとにポイント合計
        user_stats = ChoreExecution.objects.filter(
            chore__group=group,
            completed_at__gte=last_30_days,
            status='APPROVED'
        ).values('performer__username', 'performer__nickname').annotate(
            total_points=Sum('points_earned')
        ).order_by('-total_points')
        
        context['user_labels'] = [u['performer__nickname'] or u['performer__username'] for u in user_stats]
        context['user_data'] = [u['total_points'] for u in user_stats]

        # 2. 家事タスク別回数 (棒グラフ用) - 直近30日 Top 10
        chore_stats = ChoreExecution.objects.filter(
            chore__group=group,
            completed_at__gte=last_30_days,
            status='APPROVED'
        ).values('chore__title').annotate(
            count=Count('id')
        ).order_by('-count')[:10]

        context['chore_labels'] = [c['chore__title'] for c in chore_stats]
        context['chore_data'] = [c['count'] for c in chore_stats]

        return context

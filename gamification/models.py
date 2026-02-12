from django.db import models
from django.conf import settings
from accounts.models import HouseGroup

class WeeklyScore(models.Model):
    group = models.ForeignKey(HouseGroup, on_delete=models.CASCADE, related_name="weekly_scores")
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name="weekly_scores"
    )
    year = models.IntegerField()
    week_number = models.IntegerField()
    total_points = models.IntegerField(default=0)
    
    # 期間の開始・終了を保持しておくと表示に便利
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)

    class Meta:
        unique_together = ('group', 'user', 'year', 'week_number')
        ordering = ['-total_points']

    def __str__(self):
        return f"{self.year}-W{self.week_number}: {self.user} ({self.total_points}pts)"

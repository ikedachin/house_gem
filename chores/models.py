from django.db import models
from django.conf import settings
from accounts.models import HouseGroup

class Chore(models.Model):
    DIFFICULTY_CHOICES = [
        (1, '簡単 (1)'),
        (2, '普通 (2)'),
        (3, '少し大変 (3)'),
        (4, '大変 (4)'),
        (5, 'すごく大変 (5)'),
    ]

    group = models.ForeignKey(HouseGroup, on_delete=models.CASCADE, related_name="chores")
    title = models.CharField(max_length=100, verbose_name="タイトル")
    description = models.TextField(blank=True, verbose_name="詳細")
    base_points = models.IntegerField(default=10, verbose_name="基準ポイント")
    difficulty = models.IntegerField(choices=DIFFICULTY_CHOICES, default=2, verbose_name="難易度")
    
    # 属性 (簡易的にJSONで持つか、多対多にするか。MVPではChoiceFieldかCommaSeparatedで十分だが、拡張性のためJSON)
    # 例: ["strength", "dirty"]
    attributes = models.JSONField(default=list, blank=True, verbose_name="属性タグ")
    
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name="created_chores",
        verbose_name="作成者"
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} ({self.base_points}pts)"

class ChoreExecution(models.Model):
    STATUS_CHOICES = [
        ('PENDING', '承認待ち'),
        ('APPROVED', '完了'),
        ('REJECTED', '却下'),
    ]

    chore = models.ForeignKey(Chore, on_delete=models.CASCADE, related_name="executions")
    performer = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name="executions",
        verbose_name="実行者"
    )
    completed_at = models.DateTimeField(auto_now_add=True, verbose_name="完了日時")
    points_earned = models.IntegerField(verbose_name="獲得ポイント")
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='APPROVED')

    def __str__(self):
        return f"{self.chore.title} by {self.performer.nickname or self.performer.username}"

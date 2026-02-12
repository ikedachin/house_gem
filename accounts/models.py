from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.crypto import get_random_string

class HouseGroup(models.Model):
    name = models.CharField(max_length=50, verbose_name="家グループ名")
    invite_code = models.CharField(max_length=8, unique=True, verbose_name="招待コード")
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.invite_code:
            self.invite_code = get_random_string(8).upper()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class CustomUser(AbstractUser):
    nickname = models.CharField(max_length=30, verbose_name="ニックネーム", blank=True)
    house_group = models.ForeignKey(
        HouseGroup, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name="members",
        verbose_name="所属家グループ"
    )

    def __str__(self):
        return self.nickname or self.username

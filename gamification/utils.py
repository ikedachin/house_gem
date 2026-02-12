from django.utils import timezone
from .models import WeeklyScore

def update_weekly_score(user, group, points):
    """
    ユーザーの週間スコアを更新（加算）する。
    """
    today = timezone.now().date()
    # ISOカレンダーの週番号を取得 (月曜始まり)
    # 設計によると「月曜朝4時切り替え」だが、MVPでは標準のISO週番号(月曜0時切り替え)で実装する。
    year, week_num, weekday = today.isocalendar()
    
    score, created = WeeklyScore.objects.get_or_create(
        user=user,
        group=group,
        year=year,
        week_number=week_num
    )
    
    score.total_points += points
    score.save()
    return score

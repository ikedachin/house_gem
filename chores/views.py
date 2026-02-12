from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from .models import Chore, ChoreExecution
from .forms import ChoreForm
from gamification.utils import update_weekly_score

class GroupAccessMixin(UserPassesTestMixin):
    def test_func(self):
        # Viewがget_objectを持っている場合（Detail/Update/Delete）
        if hasattr(self, 'get_object'):
            chore = self.get_object()
            return chore.group == self.request.user.house_group
        return False

class ChoreListView(LoginRequiredMixin, ListView):
    model = Chore
    template_name = 'chores/chore_list.html'
    context_object_name = 'chores'

    def get_queryset(self):
        if self.request.user.house_group:
            return Chore.objects.filter(group=self.request.user.house_group).order_by('-created_at')
        return Chore.objects.none()

class ChoreCreateView(LoginRequiredMixin, CreateView):
    model = Chore
    form_class = ChoreForm
    template_name = 'chores/chore_form.html'
    success_url = reverse_lazy('chore_list')

    def form_valid(self, form):
        form.instance.group = self.request.user.house_group
        form.instance.owner = self.request.user
        return super().form_valid(form)

class ChoreUpdateView(LoginRequiredMixin, GroupAccessMixin, UpdateView):
    model = Chore
    form_class = ChoreForm
    template_name = 'chores/chore_form.html'
    success_url = reverse_lazy('chore_list')

class ChoreDeleteView(LoginRequiredMixin, GroupAccessMixin, DeleteView):
    model = Chore
    template_name = 'chores/chore_confirm_delete.html'
    success_url = reverse_lazy('chore_list')

class ChoreCompleteView(LoginRequiredMixin, GroupAccessMixin, View):
    def post(self, request, pk, *args, **kwargs):
        chore = get_object_or_404(Chore, pk=pk)
        
        # Check permission manually since we are not using SingleObjectMixin's get_object in standard way for View
        if chore.group != request.user.house_group:
            return redirect('chore_list') # Or 403

        # 1. Calculate Points
        points = chore.base_points
        
        # 2. Record Execution
        ChoreExecution.objects.create(
            chore=chore,
            performer=request.user,
            points_earned=points,
            status='APPROVED'
        )
        
        # 3. Update Weekly Score
        update_weekly_score(request.user, chore.group, points)
        
        messages.success(request, f"「{chore.title}」を完了！ {points}ポイント獲得！")
        return redirect('chore_list')

    def get_object(self):
        # For GroupAccessMixin
        return get_object_or_404(Chore, pk=self.kwargs['pk'])

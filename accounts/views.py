from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView
from django.views.generic import CreateView, FormView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import login
from .models import HouseGroup
from .forms import CustomUserCreationForm, HouseGroupForm, HouseGroupJoinForm

class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    template_name = 'accounts/signup.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('setup_group')

class CustomLoginView(LoginView):
    template_name = 'accounts/login.html'

class GroupSetupView(LoginRequiredMixin, TemplateView):
    template_name = 'accounts/group_setup.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.house_group:
            return redirect('dashboard')
        return super().dispatch(request, *args, **kwargs)

class CreateGroupView(LoginRequiredMixin, CreateView):
    model = HouseGroup
    form_class = HouseGroupForm
    template_name = 'accounts/create_group.html'
    success_url = reverse_lazy('dashboard')

    def form_valid(self, form):
        group = form.save()
        self.request.user.house_group = group
        self.request.user.save()
        return super().form_valid(form)

class JoinGroupView(LoginRequiredMixin, FormView):
    form_class = HouseGroupJoinForm
    template_name = 'accounts/join_group.html'
    success_url = reverse_lazy('dashboard')

    def form_valid(self, form):
        code = form.cleaned_data['invite_code']
        group = HouseGroup.objects.get(invite_code=code)
        self.request.user.house_group = group
        self.request.user.save()
        return super().form_valid(form)

class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'accounts/dashboard.html'
    

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.house_group:
            context['group'] = self.request.user.house_group
            context['members'] = self.request.user.house_group.members.all()
            # Recent Executions (from Chores app, needs import or reverse relation)
            # Since we can't easily import ChoreExecution here without circular dependency risk if not careful,
            # we use the related_name on User model if available, or imports.
            from chores.models import ChoreExecution
            context['executions'] = ChoreExecution.objects.filter(
                chore__group=self.request.user.house_group
            ).order_by('-completed_at')[:5]
        return context

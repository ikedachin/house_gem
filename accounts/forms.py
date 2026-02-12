from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser, HouseGroup

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ('username', 'nickname', 'email')

class HouseGroupForm(forms.ModelForm):
    class Meta:
        model = HouseGroup
        fields = ('name',)

class HouseGroupJoinForm(forms.Form):
    invite_code = forms.CharField(max_length=8, label="招待コード")

    def clean_invite_code(self):
        code = self.cleaned_data.get('invite_code')
        try:
            group = HouseGroup.objects.get(invite_code=code)
        except HouseGroup.DoesNotExist:
            raise forms.ValidationError("招待コードが無効です。")
        return code

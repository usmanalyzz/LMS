from django import forms
from .models import User


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields =('first_name', 'last_name', 'username','email', 'password', 'role', 'groups', 'user_permissions')

    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

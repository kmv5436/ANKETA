from django import forms
from django.forms import inlineformset_factory
from .models import Employee, Child


class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = [
            'full_name', 'tab_number', 'department', 'position',
            'birth_date', 'gender', 'phone_email',
            'marital_status', 'spouse_name', 'spouse_tab_number',
        ]
        widgets = {
            'birth_date': forms.DateInput(attrs={'type': 'date'}),
        }


class ChildForm(forms.ModelForm):
    class Meta:
        model = Child
        exclude = ['employee', 'family_key']
        widgets = {
            'birth_date': forms.DateInput(attrs={'type': 'date'}),
            'hobbies': forms.Textarea(attrs={'rows': 2}),
            'clubs': forms.Textarea(attrs={'rows': 3}),
            'achievements': forms.Textarea(attrs={'rows': 2}),
        }


ChildFormSet = inlineformset_factory(
    Employee,
    Child,
    form=ChildForm,
    extra=1,
    can_delete=True,
)
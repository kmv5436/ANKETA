# myanketa/forms.py
from django import forms
from django.forms import inlineformset_factory
from .models import Employee, Child


class EmployeeForm(forms.ModelForm):
    """Форма сотрудника. Подписи и сообщения — на русском."""

    class Meta:
        model = Employee
        fields = [
            'full_name', 'tab_number', 'department', 'position',
            'birth_date', 'gender', 'phone_email',
            'marital_status', 'spouse_name', 'spouse_tab_number',
        ]
        labels = {
            'full_name': 'ФИО сотрудника',
            'tab_number': 'Табельный номер',
            'department': 'Подразделение',
            'position': 'Должность',
            'birth_date': 'Дата рождения',
            'gender': 'Пол',
            'phone_email': 'Телефон / e-mail',
            'marital_status': 'Семейное положение',
            'spouse_name': 'ФИО супруга(и)',
            'spouse_tab_number': 'Табельный номер супруга(и)',
        }
        help_texts = {
            'tab_number': 'Уникальный номер сотрудника в организации.',
            'spouse_tab_number': 'Заполните, если супруг(а) работает в этой же организации.',
        }
        error_messages = {
            'full_name': {
                'required': 'Укажите ФИО сотрудника.',
                'max_length': 'ФИО слишком длинное (не более 200 символов).',
            },
            'tab_number': {
                'required': 'Укажите табельный номер.',
                'unique': 'Сотрудник с таким табельным номером уже зарегистрирован.',
                'max_length': 'Табельный номер слишком длинный (не более 20 символов).',
            },
            'birth_date': {
                'required': 'Укажите дату рождения сотрудника.',
                'invalid': 'Введите корректную дату в формате ДД.ММ.ГГГГ.',
            },
            'phone_email': {
                'max_length': 'Слишком длинное значение (не более 200 символов).',
            },
        }
        widgets = {
            'full_name': forms.TextInput(attrs={'placeholder': 'Иванов Иван Иванович'}),
            'tab_number': forms.TextInput(attrs={'placeholder': 'например, 12345'}),
            'department': forms.TextInput(attrs={'placeholder': 'Название подразделения'}),
            'position': forms.TextInput(attrs={'placeholder': 'Должность'}),
            'birth_date': forms.DateInput(attrs={'type': 'date'}, format='%Y-%m-%d'),
            'gender': forms.Select(),
            'phone_email': forms.TextInput(attrs={'placeholder': '+7 ... или e-mail'}),
            'marital_status': forms.Select(),
            'spouse_name': forms.TextInput(attrs={'placeholder': 'Петрова Мария Сергеевна'}),
            'spouse_tab_number': forms.TextInput(attrs={'placeholder': 'если работает здесь'}),
        }


class ChildForm(forms.ModelForm):
    """Форма ребёнка. Подписи и сообщения — на русском."""

    class Meta:
        model = Child
        exclude = ['employee', 'family_key']
        labels = {
            'full_name': 'ФИО ребёнка',
            'birth_date': 'Дата рождения',
            'gender': 'Пол',
            'relation': 'Родство',
            'status': 'Статус занятости',
            'school_name': 'Учебное заведение',
            'school_type': 'Тип учебного заведения',
            'faculty': 'Факультет / отделение',
            'specialty': 'Специальность / направление',
            'course': 'Курс / класс / группа',
            'edu_form': 'Форма обучения',
            'edu_level': 'Уровень образования',
            'school_address': 'Адрес / район учебного заведения',
            'needs_benefits': 'Нуждается в льготах / путёвках',
            'hobbies': 'Хобби и увлечения',
            'clubs': 'Кружки и секции',
            'achievements': 'Достижения',
        }
        help_texts = {
            'hobbies': 'Перечислите через запятую или с новой строки.',
            'clubs': 'Каждый с новой строки: Название — направление — с какого года.',
            'achievements': 'Разряды, награды, конкурсы.',
            'needs_benefits': 'Отметьте, если ребёнку требуется социальная поддержка.',
        }
        error_messages = {
            'full_name': {
                'required': 'Укажите ФИО ребёнка.',
                'max_length': 'ФИО слишком длинное (не более 200 символов).',
            },
            'birth_date': {
                'required': 'Укажите дату рождения ребёнка.',
                'invalid': 'Введите корректную дату в формате ДД.ММ.ГГГГ.',
            },
            'relation': {
                'required': 'Выберите родство.',
            },
            'status': {
                'max_length': 'Слишком длинное значение.',
            },
            'school_name': {
                'max_length': 'Название учебного заведения слишком длинное (не более 300 символов).',
            },
            'course': {
                'max_length': 'Значение слишком длинное (не более 50 символов).',
            },
        }
        widgets = {
            'full_name': forms.TextInput(attrs={'placeholder': 'Иванов Пётр Иванович'}),
            'birth_date': forms.DateInput(attrs={'type': 'date'}, format='%Y-%m-%d'),
            'gender': forms.Select(),
            'relation': forms.Select(),
            'status': forms.Select(),
            'school_name': forms.TextInput(attrs={'placeholder': 'МБОУ «Школа № 1»'}),
            'school_type': forms.TextInput(attrs={'placeholder': 'государственное / частное'}),
            'faculty': forms.TextInput(attrs={'placeholder': 'Факультет / отделение'}),
            'specialty': forms.TextInput(attrs={'placeholder': 'Специальность / направление'}),
            'course': forms.TextInput(attrs={'placeholder': 'например, 3 курс / 10 класс'}),
            'edu_form': forms.Select(),
            'edu_level': forms.Select(),
            'school_address': forms.TextInput(attrs={'placeholder': 'Адрес или район'}),
            'needs_benefits': forms.CheckboxInput(),
            'hobbies': forms.Textarea(attrs={'rows': 2, 'placeholder': 'спорт, музыка, рисование'}),
            'clubs': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Плавание — спорт — с 2020 г.'}),
            'achievements': forms.Textarea(attrs={'rows': 2, 'placeholder': 'Разряды, награды, конкурсы'}),
        }

    def clean_birth_date(self):
        """Проверка: дата рождения ребёнка не в будущем."""
        birth_date = self.cleaned_data.get('birth_date')
        if birth_date:
            from datetime import date
            if birth_date > date.today():
                raise forms.ValidationError('Дата рождения не может быть в будущем.')
        return birth_date


# Набор форм для детей, привязанный к сотруднику
ChildFormSet = inlineformset_factory(
    Employee,
    Child,
    form=ChildForm,
    extra=1,
    can_delete=True,
    min_num=0,
    validate_min=False,
)
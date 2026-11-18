from django.db import models


class Employee(models.Model):
    GENDER_CHOICES = [('M', 'М'), ('F', 'Ж')]
    MARITAL_CHOICES = [
        ('single', 'Холост / не замужем'),
        ('married', 'Женат / замужем'),
        ('divorced', 'Разведён(а)'),
        ('widowed', 'Вдова / вдовец'),
    ]

    full_name = models.CharField("ФИО сотрудника", max_length=200)
    tab_number = models.CharField("Табельный номер", max_length=20, unique=True)
    department = models.CharField("Подразделение", max_length=200, blank=True)
    position = models.CharField("Должность", max_length=200, blank=True)
    birth_date = models.DateField("Дата рождения", null=True, blank=True)
    gender = models.CharField("Пол", max_length=1, choices=GENDER_CHOICES, blank=True)
    phone_email = models.CharField("Телефон / e-mail", max_length=200, blank=True)
    marital_status = models.CharField(
        "Семейное положение", max_length=20, choices=MARITAL_CHOICES, blank=True
    )
    spouse_name = models.CharField("ФИО супруга(и)", max_length=200, blank=True)
    spouse_tab_number = models.CharField(
        "Табельный номер супруга(и)", max_length=20, blank=True,
        help_text="Если супруг(а) работает в организации"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.full_name} ({self.tab_number})"

    def family_key(self):
        """Ключ семьи для дедупликации: min из двух табельных номеров."""
        if self.spouse_tab_number:
            return min(self.tab_number, self.spouse_tab_number)
        return self.tab_number
    class Meta:
        verbose_name = 'Сотрудник'
        verbose_name_plural = 'Сотрудники'


class Child(models.Model):
    GENDER_CHOICES = [('M', 'М'), ('F', 'Ж')]
    RELATION_CHOICES = [
        ('native', 'Родной(ая)'),
        ('adopted', 'Приёмный(ая)'),
        ('guardian', 'Под опекой'),
        ('step', 'Пасынок / падчерица'),
        ('other', 'Другое'),
    ]
    STATUS_CHOICES = [
        ('preschool', 'Не организован (дошкольник)'),
        ('kindergarten', 'Детский сад'),
        ('school', 'Школа'),
        ('college', 'Колледж / техникум'),
        ('bachelor', 'Вуз (бакалавриат / специалитет)'),
        ('master', 'Вуз (магистратура)'),
        ('postgrad', 'Аспирантура'),
        ('working', 'Работает'),
        ('none', 'Не учится и не работает'),
        ('other', 'Другое'),
    ]
    EDU_LEVEL_CHOICES = [
        ('preschool', 'Дошкольное'),
        ('primary', 'Начальное'),
        ('basic', 'Основное'),
        ('secondary', 'Среднее'),
        ('vocational', 'Среднее профессиональное'),
        ('bachelor', 'Высшее (бакалавр)'),
        ('master', 'Высшее (магистр)'),
        ('other', 'Другое'),
    ]
    EDU_FORM_CHOICES = [
        ('full', 'Очная'),
        ('part', 'Заочная'),
        ('evening', 'Очно-заочная'),
        ('family', 'Семейная'),
        ('other', 'Другое'),
    ]

    employee = models.ForeignKey(
        Employee, on_delete=models.CASCADE, related_name='children'
    )
    full_name = models.CharField("ФИО ребёнка", max_length=200)
    birth_date = models.DateField("Дата рождения")
    gender = models.CharField("Пол", max_length=1, choices=GENDER_CHOICES, blank=True)
    relation = models.CharField(
        "Родство", max_length=20, choices=RELATION_CHOICES, default='native'
    )
    status = models.CharField(
        "Статус занятости", max_length=20, choices=STATUS_CHOICES, blank=True
    )
    school_name = models.CharField("Учебное заведение", max_length=300, blank=True)
    school_type = models.CharField("Тип учебного заведения", max_length=100, blank=True)
    faculty = models.CharField("Факультет / отделение", max_length=200, blank=True)
    specialty = models.CharField("Специальность / направление", max_length=200, blank=True)
    course = models.CharField("Курс / класс / группа", max_length=50, blank=True)
    edu_form = models.CharField(
        "Форма обучения", max_length=20, choices=EDU_FORM_CHOICES, blank=True
    )
    edu_level = models.CharField(
        "Уровень образования", max_length=20, choices=EDU_LEVEL_CHOICES, blank=True
    )
    school_address = models.CharField("Адрес / район учебного заведения", max_length=300, blank=True)
    needs_benefits = models.BooleanField("Нуждается в льготах / путёвках", default=False)
    hobbies = models.TextField("Хобби и увлечения", blank=True, help_text="Через запятую или с новой строки")
    clubs = models.TextField("Кружки и секции", blank=True, help_text="Каждый с новой строки: Название — направление — с какого года")
    achievements = models.TextField("Достижения", blank=True)

    # Служебное поле для дедупликации
    family_key = models.CharField(max_length=20, blank=True, db_index=True)

    def __str__(self):
        return f"{self.full_name} ({self.birth_date})"

    def save(self, *args, **kwargs):
        # Автоматически проставляем family_key на основе сотрудника
        if self.employee_id:
            self.family_key = self.employee.family_key()
        super().save(*args, **kwargs)

    def age(self):
        from datetime import date
        today = date.today()
        return today.year - self.birth_date.year - (
            (today.month, today.day) < (self.birth_date.month, self.birth_date.day)
        )
    class Meta:
        verbose_name = 'Ребёнок'
        verbose_name_plural = 'Дети'
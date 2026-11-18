from datetime import date
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib import messages
from django.db.models import Count
from openpyxl import Workbook
from openpyxl.styles import Font, Alignment

from .forms import EmployeeForm, ChildFormSet
from .models import Employee, Child


def employee_list(request):
    """Список всех сотрудников с числом детей."""
    employees = Employee.objects.annotate(children_count=Count('children')).order_by('full_name')
    return render(request, 'myanketa/employee_list.html', {'employees': employees})


def employee_create(request):
    """Создание новой анкеты сотрудника."""
    if request.method == 'POST':
        form = EmployeeForm(request.POST)
        formset = ChildFormSet(request.POST)
        if form.is_valid() and formset.is_valid():
            employee = form.save()
            formset.instance = employee
            formset.save()
            messages.success(request, f'Анкета сотрудника «{employee.full_name}» сохранена.')
            return redirect('employee_list')
    else:
        form = EmployeeForm()
        formset = ChildFormSet()
    return render(request, 'myanketa/anketa.html', {
        'form': form,
        'formset': formset,
        'title': 'Новая анкета сотрудника',
        'submit_label': 'Сохранить анкету',
    })


def employee_edit(request, pk):
    """Редактирование существующей анкеты."""
    employee = get_object_or_404(Employee, pk=pk)
    if request.method == 'POST':
        form = EmployeeForm(request.POST, instance=employee)
        formset = ChildFormSet(request.POST, instance=employee)
        if form.is_valid() and formset.is_valid():
            form.save()
            formset.save()
            messages.success(request, 'Изменения сохранены.')
            return redirect('employee_list')
    else:
        form = EmployeeForm(instance=employee)
        formset = ChildFormSet(instance=employee)
    return render(request, 'myanketa/anketa.html', {
        'form': form,
        'formset': formset,
        'title': f'Анкета: {employee.full_name}',
        'submit_label': 'Сохранить изменения',
    })


def export_excel(request):
    wb = Workbook()
    ws = wb.active
    ws.title = "Дети сотрудников"

    headers = [
        "Сотрудник", "Табельный номер", "Подразделение",
        "ФИО ребёнка", "Дата рождения", "Возраст", "Пол",
        "Родство", "Статус занятости",
        "Учебное заведение", "Факультет", "Специальность",
        "Курс / класс", "Форма обучения", "Уровень образования",
        "Нуждается в льготах", "Хобби", "Кружки", "Достижения",
    ]
    ws.append(headers)

    # Жирный заголовок
    for cell in ws[1]:
        cell.font = Font(bold=True)
        cell.alignment = Alignment(horizontal='center', wrap_text=True)

    for child in Child.objects.select_related('employee').all().order_by(
        'employee__full_name', 'birth_date'
    ):
        ws.append([
            child.employee.full_name,
            child.employee.tab_number,
            child.employee.department,
            child.full_name,
            child.birth_date.strftime('%d.%m.%Y'),
            child.age(),
            child.get_gender_display(),
            child.get_relation_display(),
            child.get_status_display(),
            child.school_name,
            child.faculty,
            child.specialty,
            child.course,
            child.get_edu_form_display(),
            child.get_edu_level_display(),
            "Да" if child.needs_benefits else "Нет",
            child.hobbies,
            child.clubs,
            child.achievements,
        ])

    # Автоширина колонок
    for column in ws.columns:
        max_len = max((len(str(cell.value)) for cell in column if cell.value), default=10)
        ws.column_dimensions[column[0].column_letter].width = min(max_len + 2, 40)

    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = (
        f'attachment; filename=children_report_{date.today():%Y%m%d}.xlsx'
    )
    wb.save(response)
    return response


def statistics_view(request):
    """Пример сводной статистики по статусам."""
    by_status = (
        Child.objects.values('status')
        .annotate(total=Count('id'))
        .order_by('-total')
    )
    # Преобразуем код статуса в человекочитаемое название
    status_dict = dict(Child.STATUS_CHOICES)
    for row in by_status:
        row['status_display'] = status_dict.get(row['status'], row['status'])

    total_children = Child.objects.count()
    total_employees = Employee.objects.count()

    return render(request, 'myanketa/statistics.html', {
        'by_status': by_status,
        'total_children': total_children,
        'total_employees': total_employees,
    })
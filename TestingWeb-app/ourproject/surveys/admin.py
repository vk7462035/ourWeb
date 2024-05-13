from django.contrib import admin
from django import forms
from .models import Survey, Question, Choice, Answer, QuestionChoice

admin.site.register(Survey)
admin.site.register(Answer)

class QuestionChoiceInline(admin.TabularInline):
    model = QuestionChoice
    extra = 1  # Количество пустых форм для добавления новых объектов

class QuestionAdminForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['text', 'survey', 'order', 'choice_type']
        widgets = {
            'choice_type': forms.RadioSelect(),  # Радио-кнопки для выбора типа выбора
        }

class QuestionAdmin(admin.ModelAdmin):
    list_display = ['text', 'survey', 'order']
    form = QuestionAdminForm
    inlines = [QuestionChoiceInline]  # Используем промежуточную модель

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        obj.save()
        form.save_m2m()  # Сохраняем ManyToMany отношения

admin.site.register(Question, QuestionAdmin)

class ChoiceAdmin(admin.ModelAdmin):
    list_display = ['id', 'choice_text']
    fields = ['choice_text']

admin.site.register(Choice, ChoiceAdmin)

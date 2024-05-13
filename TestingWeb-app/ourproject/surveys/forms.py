from django import forms
from .models import Survey, Question, Answer, Choice, QuestionChoice
from django.forms import inlineformset_factory

class SurveyForm(forms.ModelForm):
    class Meta:
        model = Survey
        fields = ['title', 'description']

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['text', 'choice_type'] #'order',
        # Добавляем виджет для поля choices
        #widgets = {
        #    'choices': forms.CheckboxSelectMultiple(),
        #}

class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ['answer_text']

AnswerFormSet = inlineformset_factory(
    Question, Answer, form=AnswerForm, extra=1, can_delete=False
)

class ChoiceForm(forms.ModelForm):
    class Meta:
        model = Choice
        fields = ['choice_text']

QuestionChoiceFormSet = inlineformset_factory(
    Question, QuestionChoice, fields=('choice',), extra=1, can_delete=True
)

QuestionFormSet = inlineformset_factory(
    Survey, Question, form=QuestionForm, extra=1, can_delete=True
)
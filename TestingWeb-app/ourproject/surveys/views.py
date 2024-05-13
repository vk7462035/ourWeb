from django.shortcuts import render, redirect
from django.views.generic import View, ListView, DetailView, CreateView
from .forms import SurveyForm, QuestionForm, AnswerFormSet
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .models import Answer, Question
from django.shortcuts import render, redirect
from django.views.generic import CreateView
from .models import Survey, Question, Choice, QuestionChoice
from .forms import SurveyForm, QuestionFormSet, QuestionChoiceFormSet

class SurveyListView(ListView):
    model = Survey
    context_object_name = 'surveys'
    template_name = 'survey_list.html'

class SurveyDetailView(DetailView):
    model = Survey
    template_name = 'survey_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = SurveyForm()
        context['questions'] = Question.objects.filter(survey=self.object).order_by('order')

        for question in context['questions']:
            if self.request.POST:
                question.answer_formset = AnswerFormSet(self.request.POST, instance=question)
            else:
                question.answer_formset = AnswerFormSet(instance=question)
        return context


class SurveyCreateView(CreateView):
    model = Survey
    form_class = SurveyForm
    template_name = 'surveys/survey_form.html'

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        if self.request.POST:
            data['questions'] = QuestionFormSet(self.request.POST)
        else:
            data['questions'] = QuestionFormSet()
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        questions = context['questions']
        self.object = form.save()

        if questions.is_valid():
            questions.instance = self.object
            questions.save()

            for question_form in questions:
                question = question_form.instance

                # Получение текстов ответов
                choices_data = self.request.POST.getlist(f'questions-{question_form.prefix}-choices-choice_text')
                for choice_text in choices_data:
                    if choice_text.strip():
                        # Сохранение Choice
                        choice, created = Choice.objects.get_or_create(choice_text=choice_text)

                        # Создание связи в QuestionChoice
                        QuestionChoice.objects.get_or_create(question=question, choice=choice)

        return super().form_valid(form)

    def get_success_url(self):
        return reverse('survey_create')

class QuestionCreateView(CreateView):
    model = Question
    form_class = QuestionForm
    template_name = 'question_form.html'

    def form_valid(self, form):
        form.instance.survey_id = self.kwargs['pk']
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('survey_detail', kwargs={'pk': self.kwargs['pk']})

class AnswerSubmitView(View):
    def post(self, request, *args, **kwargs):
        survey = Survey.objects.get(pk=kwargs['pk'])
        for key, value in request.POST.items():
            if key.startswith('question_'):
                question_id = int(key.split('_')[2])
                question = Question.objects.get(id=question_id)
                Answer.objects.create(question=question, answer_text=value)
        return redirect('survey_list')

# Определяем функцию для отправки ответа на вопрос
@login_required
def submit_answer(request, question_id):
    if request.method == 'POST':
        question = Question.objects.get(pk=question_id)
        answer_text = request.POST.get('answer_text')  # Предполагается, что вы получаете текст ответа из формы
        user = request.user  # Получаем текущего пользователя

        # Создаем объект ответа и сохраняем его в базу данных
        Answer.objects.create(question=question, answer_text=answer_text, user=user)

        # Перенаправляем пользователя после отправки ответа
        return redirect('survey_detail', pk=question.survey.pk)
    else:
        # Обработка GET запроса (вы можете добавить свою логику)
        pass
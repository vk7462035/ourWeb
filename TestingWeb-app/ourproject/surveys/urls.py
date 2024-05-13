from django.urls import path
from .views import SurveyListView, SurveyDetailView, SurveyCreateView, QuestionCreateView, AnswerSubmitView

urlpatterns = [
    path('surveys/', SurveyListView.as_view(), name='survey_list'),
    path('survey/<int:pk>/', SurveyDetailView.as_view(), name='survey_detail'),
    path('create_survey/', SurveyCreateView.as_view(), name='create_survey'),
    path('survey/<int:pk>/add_question/', QuestionCreateView.as_view(), name='add_question'),
    path('survey/<int:pk>/submit_answers/', AnswerSubmitView.as_view(), name='submit_answers'),
    path('create/', SurveyCreateView.as_view(), name='survey_create'),
]


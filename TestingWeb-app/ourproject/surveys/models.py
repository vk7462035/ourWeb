from django.db import models
from django.contrib.auth.models import User

class Survey(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()

    def __str__(self):
        return self.title

class Choice(models.Model):
    choice_text = models.CharField(max_length=300)

    def __str__(self):
        return self.choice_text

class Question(models.Model):
    survey = models.ForeignKey(Survey, related_name='questions', on_delete=models.CASCADE)
    text = models.CharField(max_length=300)
    order = models.IntegerField(default=0)
    choices = models.ManyToManyField(Choice, through='QuestionChoice', related_name='questions')

    SINGLE_CHOICE = 'single'
    MULTIPLE_CHOICE = 'multiple'
    CHOICE_TYPE_CHOICES = [
        (SINGLE_CHOICE, 'Выбор только одного ответа'),
        (MULTIPLE_CHOICE, 'Выбор нескольких ответов'),
    ]
    choice_type = models.CharField(max_length=20, choices=CHOICE_TYPE_CHOICES, default=SINGLE_CHOICE)

    def __str__(self):
        return self.text

class QuestionChoice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice = models.ForeignKey(Choice, on_delete=models.CASCADE)

class Answer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    question = models.ForeignKey(Question, related_name='answers', on_delete=models.CASCADE)
    answer_text = models.CharField(max_length=300)

    def __str__(self):
        return f"Answer by {self.user.username} to question: {self.question.text}"

import datetime
from django.shortcuts import render
from django.views.generic import ListView
from .models import Question

# Create your views here.


# =================== Просмотр списка незавершенных вопросов для голосования =======================
class ListQuestion4VotingView(ListView):
    template_name = 'questions.html'
    date = datetime.date.today()
    queryset = Question.objects.filter(date_end__gte=date)
    context_object_name = 'questions'
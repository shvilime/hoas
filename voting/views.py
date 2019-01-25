import datetime
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, View
from .models import Question
from .forms import AddCandidateForm

# Create your views here.


# =================== Просмотр списка незавершенных вопросов для голосования =======================
class ListQuestion4VotingView(ListView):
    template_name = 'questions.html'
    date = datetime.date.today()
    queryset = Question.objects.filter(date_end__gte=date)
    context_object_name = 'questions'


# ======================= Детализированный просмотр вопроса и голосование ==========================
class DetailQuestionView(View):
    template_name = 'questiondetail.html'
    context = {'addcandidateform': AddCandidateForm,
               'question': None,
               'candidates': None}

    def get(self, request, *args, **kwargs):
        self.context['addcandidateform'] = AddCandidateForm()
        self.context['question'] = get_object_or_404(Question, pk=kwargs.get('pk', None))
        self.context['candidates'] = self.context['question'].candidates.all()
        return render(request, self.template_name, self.context)

    def post(self, request, *args, **kwargs):
        return render(request, self.template_name, self.context)
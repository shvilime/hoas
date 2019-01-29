import datetime
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.shortcuts import render, HttpResponseRedirect, get_object_or_404
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
        self.context['question'] = get_object_or_404(Question, pk=kwargs.get('pk', None))
        self.context['candidates'] = self.context['question'].candidates.all()
        self.context['addcandidateform'] = AddCandidateForm(initial={'nominator': request.user,
                                                                     'question': self.context['question']})
        return render(request, self.template_name, self.context)

    def post(self, request, *args, **kwargs):
        self.context['addcandidateform'] = AddCandidateForm(request.POST)
        if self.context['addcandidateform'].is_valid():
            self.context['addcandidateform'].save()
            messages.info(request, 'Кандидатура добавлена', 'icon-user')
            HttpResponseRedirect(self.request.path_info)
        return render(request, self.template_name, self.context)
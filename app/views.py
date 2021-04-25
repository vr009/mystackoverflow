from django.shortcuts import render
from .models import Profile, Question, Tag, Like, Answer
from django.http import Http404
from django.core.paginator import Paginator, EmptyPage

OBJ_NUM = 5     #константа на количество объектов на странице


def paginate(object_list, page_num,  request, signed_up=False, per_page=5):
    if per_page > 10:
        per_page = 10

    paginator = Paginator(object_list, per_page)
    try:
        page = paginator.page(page_num)
    except EmptyPage:
        page = Paginator.page(paginator.num_pages)

    return page


class Abs:
    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('views.index', args=[str(self.id)])



# список новых вопросов
def index(request):
    questions = Question.objects.new(OBJ_NUM)
    for question in questions:
        question.rating = Like.objects.filter(id_question=question).count()
    return render(request, 'index.html', {'questions': questions, 'signed_up': True, 'abs':Abs})

#список горячих вопросов
def hot(request):
    questions = Question.objects.hot(OBJ_NUM)
    for question in questions:
        question.rating = Like.objects.filter(id_question=question).count()
    return render(request, 'hot.html', {'questions': questions, 'signed_up': True, 'abs':Abs})

#список вопросов по тегу
def onetag(request, tag):
    questions = Question.objects.by_tag(tag, OBJ_NUM)
    if questions.count() == 0:
        raise Http404("No questions by this tag")
    return render(request, 'onetag.html', {'questions': questions , 'signed_up': True, 'abs':Abs})


def ask(request):
    return render(request, 'ask.html', {'signed_up': True})

def login(request):
    return render(request, 'login.html', {'signed_up': True})

def settings(request):
    return render(request, 'settings.html', {'signed_up': True})

def signup(request):
    return render(request, 'signup.html', {'signed_up': False})

def one_question(request, pk: int):
    try:
        question = Question.objects.get(id=pk)
    except question.DoesNotExist:
        raise Http404

    answers = Answer.objects.by_question(pk)
    return render(request, 'question.html', {"question": question, "answers": answers, 'signed_up': True})
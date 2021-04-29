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
        page = paginator.page(paginator.num_pages)
        # raise Http404

    return page


# список новых вопросов
def index(request,pk = 1):
    questions = Question.objects.new()
    Like.objects.like_count(questions)
    pg = paginate(questions,pk,request,True,6)
    return render(request, 'index.html', {'questions': pg.object_list, 'signed_up': True})


#список горячих вопросов
def hot(request, pk = 1):
    questions = Question.objects.hot()
    Like.objects.like_count(questions)
    pg = paginate(questions,pk,request,True,6)
    return render(request, 'hot.html', {'questions': pg.object_list, 'signed_up': True})


#список вопросов по тегу
def onetag(request, tag, pk=1):
    questions = Question.objects.by_tag(tag, OBJ_NUM)

    if questions.count() == 0:
        raise Http404("No questions by this tag")

    pg = paginate(questions,pk,request,True)
    return render(request, 'onetag.html', {'questions': pg.object_list , 'signed_up': True})


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

    answers = paginate(Answer.objects.by_question(pk),1,request,True).object_list
    return render(request, 'question.html', {"question": question, "answers": answers, 'signed_up': True})
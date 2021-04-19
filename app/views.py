from django.shortcuts import render
from .models import Profile, Question, Tag, Like, Answer

tags = ["favorite language", "the best os", "linux", "microsoft", "github", "docker"]

users = ["dart vader", "obi-wan kenobi", "Palpatine", "Luke skywalker"]

pics = [ "dartvader.jpg", "obi_wan.jpg", "sidious.jpg", "luke.jpg" ]

questions = [
    {
        'id': idx,
        'tag': tags[idx],
        'user': users[idx],
        'pic': "/static/img/" + pics[idx],       # a bit hard code
        'title': f'favourite os',
        'text': f'Some text for question #{idx}'
    } for idx in range(len(users))
]

answers = [
    {
        'id': idx,
        'tag': tags[idx],
        'user': users[idx],
        'pic': "/static/img/" + pics[idx],       # a bit hard code
        'title': f'favourite osblablablabla' ,
        'text': f'In my opinion that depends on #{idx} '*6
    } for idx in range(len(users))
]



# список новых вопросов
def index(request):
    questions = Question.objects.new()
    return render(request, 'index.html', {'questions': questions})

#список горячих вопросов
def hot(request):
    questions = Question.objects.hot()
    return render(request, 'hot.html', {'questions': questions})

#список вопросов по тегу
def onetag(request, tag):
    questions = Question.objects.by_tag(tag)
    return render(request, 'onetag.html', {'questions': questions })


def ask(request):
    return render(request, 'ask.html', {})

def login(request):
    return render(request, 'login.html', {})

def settings(request):
    return render(request, 'settings.html', {})

def signup(request):
    return render(request, 'signup.html', {})

def tagpage(request):
    return render(request, 'tagpage.html', {})

def one_question(request, pk: int):
    question = Question.objects.filter(id=pk)
    answers = Answer.objects.by_question(pk)
    return render(request, 'question.html', {"question": question, "answers": answers})
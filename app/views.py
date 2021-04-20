from django.shortcuts import render
from django.db.models import ImageField
from .models import Profile, Question, Tag, Like, Answer
from django.http import Http404
from django.contrib.auth.models import User
from django.utils import timezone
OBJ_NUM = 5

pic = ImageField("luke.jpg")

usernames = set(list(User.objects.values_list('username', flat=True)))
my_tag = Tag(name="macos")
my_tag.save()


for i in range(10000):
    usrname = str(i)
    if usrname not in usernames:
        n_user = User(username=usrname,password="12345_top")
        n_profile = Profile(user=n_user, name=usrname,avatar="luke.jpg")
        n_user.save()
        n_profile.save()
        for j in range(10):
            question = Question(title="wtf?", text="sdasdsasdasd", rating=12,date=timezone.now(), author=n_user)
            question.save()




def paginate(object_list, signed_up:bool, request, per_page=5):
    pass

# список новых вопросов
def index(request):
    questions = Question.objects.new(OBJ_NUM)
    return render(request, 'index.html', {'questions': questions, 'signed_up': True})

#список горячих вопросов
def hot(request):
    questions = Question.objects.hot(OBJ_NUM)
    return render(request, 'hot.html', {'questions': questions, 'signed_up': True})

#список вопросов по тегу
def onetag(request, tag):
    questions = Question.objects.by_tag(tag, OBJ_NUM)
    if questions.count() == 0:
        raise Http404("No questions by this tag")
    return render(request, 'onetag.html', {'questions': questions , 'signed_up': True})


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
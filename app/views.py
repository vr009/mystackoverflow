from django.shortcuts import render, redirect
from .models import Profile, Question, Tag, Like, Answer
from django.http import HttpResponseRedirect, JsonResponse, Http404
from django.core.paginator import Paginator, EmptyPage
from django.db import IntegrityError
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import auth
from .forms import QuestionForm, AnswerForm, RegistrationForm, loginForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

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
def index(request, pk=1):
    questions = Question.objects.new()
    Like.objects.like_count(questions)
    pg = paginate(questions, pk, request, True, 6)
    return render(request, 'index.html', {'questions': pg.object_list, 'signed_up': True})


#список горячих вопросов
def hot(request, pk=1):
    questions = Question.objects.hot()
    Like.objects.like_count(questions)
    pg = paginate(questions, pk, request, True, 6)
    return render(request, 'hot.html', {'questions': pg.object_list, 'signed_up': True})


#список вопросов по тегу
def onetag(request, tag, pk=1):
    questions = Question.objects.by_tag(tag)

    if questions.count() == 0:
        raise Http404("No questions by this tag")

    pg = paginate(questions, pk, request, True)
    return render(request, 'onetag.html', {'questions': pg.object_list, 'signed_up': True, 'tag_name': tag})



@login_required
def ask(request):
    if not request.user.is_authenticated:
        return JsonResponse({'status': 'error', 'message': 'Ошибка доступа'})
    if request.method == "POST":
        form = QuestionForm(request.POST)
        if form.is_valid():
            quest = Question.objects.create(title=request.POST.get('title'), text=request.POST.get('text'),
                                            author=request.user)
            tags = request.POST.get('tags').split(",")
            for tag in tags:
                tag = (str(tag)).replace(' ', '')
                Tag.objects.add_qst(tag, quest)
            quest.save()
            return HttpResponseRedirect('/question/{}/'.format(quest.id))
        return render(request, 'ask.html', {'form': form})
    form = QuestionForm()
    return render(request, 'ask.html', {'form': form})


def login(request):
    # new_pth = request.GET
    if request.method == "GET":
        form = loginForm
    if request.method == "POST":
        form = loginForm(data=request.POST)
        if form.is_valid():
            user = auth.authenticate(request, username=request.POST.get('username'), password=request.POST.get('password'))

            if user is not None:
                # print(new_pth)
                auth.login(request, user)
                return redirect('/')

    return render(request, 'login.html', {'signed_up': True, 'form': form})

def logout(request):
    if request.user.is_authenticated:
        auth.logout(request)
    return HttpResponseRedirect('/?continue=logout')

@login_required
def settings(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            form = RegistrationForm(request.POST)
            if form.is_valid():
                data = get_data(request)
                request.user.username = data['username']
                request.user.set_password(data['password'])
                request.user.email = data['email']
                request.user.first_name = data['first_name']
                request.user.last_name = data['last_name']
                if data['avatar']:
                    request.user.userprofile.avatar = data['avatar']
                request.user.save()
                request.user.profile.save()
                user = auth.authenticate(username=data['username'], password=data['password'])
                if user is not None:
                    auth.login(request, user)

            return render(request, 'settings.html', {'form': form})
        # auto filed
        user_data = User.objects.get(id=request.user.id)
        first_name = user_data.first_name
        last_name = user_data.last_name
        username = user_data.username
        email = user_data.email
        form = RegistrationForm({'first_name': first_name, 'last_name': last_name, 'username': username,
                                 'email': email})
        return render(request, 'settings.html', {'form': form})
    return HttpResponseRedirect('/?continue=notlogin')


def signup(request):
    if request.method == "GET":
        form = RegistrationForm
    if request.method == "POST":
        form = RegistrationForm(data=request.POST)

        if form.is_valid():
            data = get_data(request)
            try:
                user = User.objects.create_user(username=data['username'], email=data['email'],
                                                password=data['password'])
                # user.first_name = data['first_name']
                # user.last_name = data['last_name']
                # user.save()
                user_pk = User.objects.get(id=user.pk)
                add_avatar = Profile(user=user_pk, name=user.username, avatar=data['avatar'])
                add_avatar.save()


                return HttpResponseRedirect('/login/')
            except IntegrityError:
                print(IntegrityError)
                return render(request, 'signup.html', {'form': form})

    return render(request, 'signup.html', {'form': form, 'signed_up': False})



def one_question(request, pk:int):
    try:
        question = Question.objects.get(id=pk)
    except question.DoesNotExist:
        raise Http404

    if request.method == "GET":
        form = AnswerForm
    if request.method == "POST":
        form = AnswerForm(data=request.POST)

        if form.is_valid():
            data = get_data(request)
            if form.is_valid():
                data = get_data(request)
                answer = Answer.objects.create(question=question, user=request.user, body=request.POST['text'])
                return HttpResponseRedirect('/question/' + str(pk) + '/')

    answers = paginate(Answer.objects.by_question(pk), 1, request, True).object_list

    return render(request, 'question.html', {"question": question, "answers": answers, "answerForm": form})


def get_data(request):
    data = dict()
    data['first_name'] = request.POST.get("first_name")
    data['last_name'] = request.POST.get("last_name")
    data['username'] = request.POST.get("username")
    data['email'] = request.POST.get("email")
    data['password'] = request.POST.get("password")
    data['password2'] = request.POST.get("password2")
    data['avatar'] = request.FILES.get("avatar")
    return data



@csrf_exempt
def add_like(request):
    if request.method == 'POST':
        ans_id = request.POST['answer_id']
        questions = Question.objects.get(pk=ans_id)
        like_dis = request.POST['answer']
        if check(request, like_dis, questions):
            print("HERE")
            return JsonResponse({'rating': questions.rating})
        return JsonResponse({'rating': questions.rating})



def check(request, like_dis, questions):
    try:

        Like.objects.get(id_question=questions, id_user=request.user, value=True)
        return False
    except ObjectDoesNotExist:
        if like_dis == 'like':

            questions.rating = questions.rating + 1
            questions.save()
        else:
            questions.rating = questions.rating - 1
            questions.save()
        like = Like(id_question=questions, id_user=request.user, value=True)
        like.save()
        return True

@csrf_exempt
def is_correct(request):
    if request.method == 'POST':
        ans_id = request.POST['answer_id']
        answer = Answer.objects.get(pk=ans_id)
        if answer.author_id == request.user.id:
            answer.is_correct = not answer.is_correct
            answer.save()
        return JsonResponse({'status': "ok"})

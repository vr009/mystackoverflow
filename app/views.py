from django.shortcuts import render


tags = ["favorite language", "the best os", "linux", "microsoft", "github", "docker"]

users = ["dart vader", "obi-wan kenobi", "Palpatine", "Luke skywalker"]

questions = [
    {
        'id': idx,
        'tag': tags[idx],
        'user': users[idx],
        'title': f'favourite os',
        'text': f'Some text for question #{idx}'
    } for idx in range(4)
]



# Create your views here.
def index(request):
    return render(request, 'index.html', {'questions': questions})

def hot(request):
    return render(request, 'hot.html', {'questions': questions})

def onetag(request):
    return render(request, 'onetag.html', {'questions': questions, 'tags': tags })


def ask(request):
    return render(request, 'ask.html', {})

def login(request):
    return render(request, 'login.html', {})

def question(request):
    return render(request, 'question.html', {})

def settings(request):
    return render(request, 'settings.html', {})

def signup(request):
    return render(request, 'signup.html', {})

def tagpage(request):
    return render(request, 'tagpage.html', {})

def one_question(request, pk):
    question = questions[pk]
    return render(request, 'question.html', {"question": question, "users": users})
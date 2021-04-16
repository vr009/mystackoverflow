from django.shortcuts import render


questions = [
    {
        'id': idx,
        'title': f'Title number {idx}',
        'text': f'Some text for question #{idx}'
    } for idx in range(4)

]
# Create your views here.
def index(request):
    return render(request, 'index.html', {'questions': questions})

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
    return render(request, 'index.html', {"question": question})
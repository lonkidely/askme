from django.shortcuts import render

# Create your views here.
def main_page(request):
    return render(request, 'index.html')

def question_page(request):
    return render(request, 'question.html')

def new_question_page(request):
    return render(request, 'new_question.html')

def tag_page(request):
    return render(request, 'tag_page.html')

def register_page(request):
    return render(request, 'register.html')

def login_page(request):
    return render(request, 'login.html')

def user_settings_page(request):
    return render(request, 'user_settings.html')

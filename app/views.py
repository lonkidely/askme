from django.shortcuts import render, get_object_or_404
from app.models import Question, Answer, Author, Tag
from django.contrib import auth
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator


def paginate(object_list, request, per_page=10):
    paginator = Paginator(object_list, per_page)
    page_number = request.GET.get('page')
    return paginator.get_page(page_number)


def new_questions_page(request):
    questions = Question.objects.new().all().prefetch_related('author', 'tags')
    page = paginate(questions, request)
    tags = Tag.objects.popular_tags()
    members = Author.objects.popular_authors()
    return render(request, 'index.html', {
        'page': page,
        'type': 'new',
        'short': True,
        'page_end_diff': page.paginator.num_pages - page.number,
        'tags': tags,
        'members': members
    })


def hot_questions_page(request):
    questions = Question.objects.hot().all().prefetch_related('author', 'tags')
    page = paginate(questions, request)
    tags = Tag.objects.popular_tags()
    members = Author.objects.popular_authors()
    return render(request, 'index.html', {
        'page': page,
        'type': 'hot',
        'short': True,
        'page_end_diff': page.paginator.num_pages - page.number,
        'tags': tags,
        'members': members
    })


def question_page(request, number):
    question = get_object_or_404(Question, id=number)

    tags = Tag.objects.popular_tags()
    members = Author.objects.popular_authors()

    answers = paginate(Answer.objects.answers(number), request, 5)
    return render(request, 'question.html', {
        'question': question,
        'short': False,
        'page': answers,
        'comments': answers,
        'page_end_diff': answers.paginator.num_pages - answers.number,
        'tags': tags,
        'members': members
    })


def new_question_page(request):
    return render(request, 'ask.html')


def tag_page(request, tag):
    questions = Question.objects.search_by_tag(tag).all().prefetch_related('author', 'tags')
    page = paginate(questions, request)
    tags = Tag.objects.popular_tags()
    members = Author.objects.popular_authors()
    return render(request, 'index.html', {
        'page': page,
        'short': True,
        'page_end_diff': page.paginator.num_pages - page.number,
        'tags': tags,
        'members': members
    })


def register_page(request):
    return render(request, 'signup.html')


def login_page(request):
    return render(request, 'login.html')


def user_settings_page(request):
    return render(request, 'user_settings.html')

def not_found_page(request, exception):
    return render(request, '404_page.html', status=404)

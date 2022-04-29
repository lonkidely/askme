from django.db import models
from django.contrib.auth.models import User

def upload_avatar(instance, filename):
    return 'avatars/{}/{}'.format(instance.user.id, filename)


class AuthorManager(models.Manager):
    def popular_authors(self):
        return self.order_by('-count_posts')[:10]


class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='author')
    nickname = models.CharField(max_length=32, verbose_name='nickname', default='Typical user')
    avatar = models.ImageField(upload_to=upload_avatar, default='avatars/avatar.png', verbose_name='avatar')
    count_posts = models.IntegerField(default=0, verbose_name='Question and answers count')

    objects = AuthorManager()

    def __str__(self):
        return self.nickname

    class Meta:
        verbose_name = 'Author'
        verbose_name_plural = 'Autors'
        ordering = ['id']


class TagManager(models.Manager):
    def popular_tags(self):
        return self.order_by('-count_questions')[:10]


class Tag(models.Model):
    title = models.CharField(max_length=16, unique=True, verbose_name='Tag title')
    count_questions = models.IntegerField(default=0, verbose_name='Questions with this tag count')

    objects = TagManager()

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Tag'
        verbose_name_plural = 'Tags'


class QuestionManager(models.Manager):
    def new(self):
        return self.order_by('-published_date')

    def hot(self):
        return self.order_by('-rating')

    def search_by_tag(self, tag):
        return self.filter(tags__title=tag)

    def one_question(self, pk):
        return self.filter(id=pk)


class Question(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    title = models.CharField(max_length=128, verbose_name='Title')
    content = models.TextField(verbose_name='Content')
    published_date = models.DateField(auto_now_add=True, verbose_name='Published date')
    tags = models.ManyToManyField(Tag, verbose_name='Tags', blank=True)
    rating = models.IntegerField(default=0, verbose_name='Rating')

    objects = QuestionManager()

    def answers_count(self):
        return Answer.objects.answers_count(self.id)

    def all_tags(self):
        return self.tags.all()

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Question'
        verbose_name_plural = 'Questions'


class AnswerManager(models.Manager):
    def answers(self, question_id):
        return self.filter(related_question__id=question_id).order_by('-rating')

    def answers_count(self, question_id):
        return self.filter(related_question__id=question_id).count()


class Answer(models.Model):
    related_question = models.ForeignKey(Question, on_delete=models.CASCADE, verbose_name='question')
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    content = models.TextField(max_length=256, verbose_name='content')
    rating = models.IntegerField(default=0, verbose_name='Rating')

    objects = AnswerManager()

    def __str__(self):
        if len(self.content) > 32:
            return self.content[:29] + '...'
        return self.content

    class Meta:
        verbose_name = 'Answer'
        verbose_name_plural = 'Answers'


class LikeQuestion(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE, verbose_name='User that liked')
    question = models.ForeignKey(Question, on_delete=models.CASCADE, verbose_name='Question')
    state = models.BooleanField(null=True, verbose_name='Like or dislike')

    def __str__(self):
        return ('Like' if self.state == 1 else 'Dislike') + \
               ' by user ' + self.author.nickname + \
               ' on question ' + self.question.title

    class Meta:
        verbose_name = 'Like or dislike on question'
        verbose_name_plural = 'Likes or dislikes on questions'
        unique_together = ['author', 'question']


class LikeAnswer(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE, verbose_name='User that liked')
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE, verbose_name='Answer')
    state = models.BooleanField(null=True, verbose_name='Like or dislike')

    def __str__(self):
        return ('Like' if self.state == 1 else 'Dislike') + \
               ' by user ' + self.author.nickname + \
               ' on answer: ' + self.answer.content[:10] + '...'

    class Meta:
        verbose_name = 'Like or dislike on answer'
        verbose_name_plural = 'Likes or dislike on answers'
        unique_together = ['author', 'answer']

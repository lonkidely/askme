from django.core.management.base import BaseCommand
from app.models import Question, Author, Tag, Answer, LikeAnswer, LikeQuestion
from django.contrib.auth.models import User
from random import randint, choice, choices
from itertools import islice
from faker import Faker

f = Faker(['en-US'])
Faker.seed(1259811)

small = [100, 100, 1000, 10000, 10000, 10000]
medium = [2000, 2000, 20000, 200000, 200000, 200000]
large = [20000, 20000, 200000, 2000000, 2000000, 2000000]


class Command(BaseCommand):
    help = 'This command fill database'

    def add_arguments(self, parser):
        parser.add_argument('-s', '--db_size', type=str, help='Database size: small, medium, large')
        parser.add_argument('-u', '--users', type=int, help='Users amount')
        parser.add_argument('-t', '--tags', type=int, help='Tags amount')
        parser.add_argument('-q', '--question', type=int, help='Questions amount')
        parser.add_argument('-a', '--answer', type=int, help='Answers amount')
        parser.add_argument('--likes_questions', type=int, help='Questions likes amount')
        parser.add_argument('--likes_answers', type=int, help='Answers likes amount')

    def write_to_db(self, Obj, objs):
        slice_size = 1000
        while True:
            slices = list(islice(objs, slice_size))
            if not slices:
                break
            Obj.objects.bulk_create(slices, slice_size)

    def fill_authors(self, amount):
        if amount is None:
            return

        users = (
            User(
                username=f.unique.name(),
                email=f.unique.email()
            ) for i in range(amount)
        )

        self.write_to_db(User, users)

        users_id = list(User.objects.values_list('id', flat=True))
        authors = (
            Author(
                user_id=users_id[i],
                avatar='avatars/avatar.png',
                nickname=f.name()
            ) for i in range(amount)
        )
        self.write_to_db(Author, authors)

    def fill_tags(self, amount):
        if amount is None:
            return

        tags = (
            Tag(
                title='Tag' + str(f.unique.random_int(min=0, max=200000))
            ) for i in range(amount)
        )
        self.write_to_db(Tag, tags)

    def fill_questions(self, amount):
        if amount is None:
            return

        author_ids = list(Author.objects.values_list('id', flat=True))
        author_posts_count = dict.fromkeys(author_ids, 0)
        authors = choices(author_ids, k=amount)

        questions = (
            Question(
                author_id=authors[i],
                title=f.sentence(nb_words=5)[:128],
                content=' '.join(f.sentences(f.random_int(min=3, max=10))),
                published_date=f.date_time_this_month(),
            ) for i in range(amount)
        )
        self.write_to_db(Question, questions)

        tags_id = list(Tag.objects.values_list('id', flat=True))
        tags_count_questions = dict.fromkeys(tags_id, 0)

        for question in Question.objects.all():
            author_posts_count[question.author.id] += 1
            for tag in set(choices(tags_id, k=randint(1, 3))):
                tags_count_questions[tag] += 1
                question.tags.add(tag)

        tags_list = list(Tag.objects.all())
        for tag in tags_list:
            tag.count_questions = tags_count_questions[tag.pk]

        authors_list = list(Author.objects.all())
        for author in authors_list:
            author.count_posts = author_posts_count[author.pk]

        Tag.objects.bulk_update(tags_list, ['count_questions'])
        Author.objects.bulk_update(authors_list, ['count_posts'])

    def fill_answers(self, amount):
        if amount is None:
            return

        question_ids = list(Question.objects.values_list('id', flat=True))
        author_ids = list(Author.objects.values_list('id', flat=True))
        authors = choices(author_ids, k=amount)

        answers = (
            Answer(
                related_question_id=choice(question_ids),
                author_id=authors[i],
                content=' '.join(f.sentences(f.random_int(min=2, max=5)))
            ) for i in range(amount)
        )
        self.write_to_db(Answer, answers)

        authors_posts_count = dict.fromkeys(author_ids, 0)
        for i in authors:
            authors_posts_count[i] += 1

        authors_list = list(Author.objects.all())
        for author in authors_list:
            author.count_posts += authors_posts_count[author.pk]
        Author.objects.bulk_update(authors_list, ['count_posts'])

    def fill_likes_questions(self, amount):
        if amount is None:
            return

        authors_id = list(Author.objects.values_list('id', flat=True))
        questions_id = list(Question.objects.values_list('id', flat=True))

        questions = choices(questions_id, k=amount)
        states = choices([True, False, False, True, False, False, False, True, True, True], k=amount)
        likes = (
            LikeQuestion(
                author_id=choice(authors_id),
                question_id=questions[i],
                state=states[i]
            ) for i in range(amount)
        )
        self.write_to_db(LikeQuestion, likes)

        questions_rating = dict.fromkeys(questions_id, 0)
        for i in range(amount):
            if states[i]:
                questions_rating[questions[i]] += 1
            else:
                questions_rating[questions[i]] -= 1

        questions_list = list(Question.objects.all())
        for question in questions_list:
            question.rating = questions_rating[question.pk]
        Question.objects.bulk_update(questions_list, ['rating'])

    def fill_likes_answers(self, amount):
        if amount is None:
            return

        authors_id = list(Author.objects.values_list('id', flat=True))
        answers_id = list(Answer.objects.values_list('id', flat=True))

        answers = choices(answers_id, k=amount)
        states = choices([True, False, False, True, False, False, False, True, True, True], k=amount)
        likes = (
            LikeAnswer(
                author_id=choice(authors_id),
                answer_id=answers[i],
                state=states[i]
            ) for i in range(amount)
        )
        self.write_to_db(LikeAnswer, likes)

        answers_rating = dict.fromkeys(answers_id, 0)
        for i in range(amount):
            if states[i]:
                answers_rating[answers[i]] += 1
            else:
                answers_rating[answers[i]] -= 1

        answers_list = list(Answer.objects.all())
        for answer in answers_list:
            answer.rating = answers_rating[answer.pk]
        Answer.objects.bulk_update(answers_list, ['rating'])

    def handle(self, *args, **options):
        data_size = [
            options.get('authors'),
            options.get('tags'),
            options.get('questions'),
            options.get('answers'),
            options.get('likes_questions'),
            options.get('likes_answers')
        ]

        db_size = options.get('db_size')
        if db_size == 'small':
            data_size = small
        elif db_size == 'medium':
            data_size = medium
        elif db_size == 'large':
            data_size = large

        self.fill_authors(data_size[0])
        self.fill_tags(data_size[1])
        self.fill_questions(data_size[2])
        self.fill_answers(data_size[3])
        self.fill_likes_questions(data_size[4])
        self.fill_likes_answers(data_size[5])

        print('Filling database finished')

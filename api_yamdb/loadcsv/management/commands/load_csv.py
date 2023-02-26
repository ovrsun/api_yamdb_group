import csv
from django.core.management import BaseCommand
from reviews.models import Category, Comment, Genre, Title, Review, Genre_Title
from users.models import CustomUser


class Command(BaseCommand):
    help = 'description'

    def categories_load(self):
        file_path = 'static/data/category.csv'
        with open(file_path, "r") as csv_file:
            data = list(csv.reader(csv_file, delimiter=","))
            for row in data[1:]:
                Category.objects.create(name=row[1], slug=row[2])  # Давайте перепишем на bulk_create, иначе будем грустно делать кучу запросов, если файлы будут большими

    def genres_load(self):
        file_path = 'static/data/genre.csv'
        with open(file_path, "r") as csv_file:
            data = list(csv.DictReader(csv_file, delimiter=","))
            for row in data:
                Genre.objects.create(name=row['name'], slug=row['slug'])

    def users_load(self):
        file_path = 'static/data/users.csv'
        with open(file_path, "r") as csv_file:
            data = list(csv.DictReader(csv_file, delimiter=","))
            for row in data:
                CustomUser.objects.create(
                    username=row['username'],
                    email=row['email'],
                    role=row['role'],
                    bio=row['bio'],
                    first_name=row['first_name'],
                    last_name=row['last_name'],
                )

    def titles_load(self):
        file_path = 'static/data/titles.csv'
        with open(file_path, "r") as csv_file:
            data = list(csv.DictReader(csv_file, delimiter=","))
            for row in data:
                try:
                    category, _ = Category.objects.get_or_create(
                        pk=row['category']
                    )
                    num = row['category']
                    category = Category.objects.get(pk=num)
                    Title.objects.create(
                        name=row['name'],
                        year=row['year'],
                        category_id=category.id
                    )
                except Category.DoesNotExist as e:
                    print(e)

    def reviews_load(self):
        file_path = 'static/data/review.csv'
        with open(file_path, "r") as csv_file:
            data = list(csv.DictReader(csv_file, delimiter=","))
            for row in data:
                title, _ = Title.objects.get_or_create(pk=row['title_id'])
                author = CustomUser.objects.get(pk=row['author'])
                Review.objects.create(
                    title=title,
                    text=row['text'],
                    author_id=author.id,
                    score=row['score'],
                    pub_date=row['pub_date']
                )

    def comments_load(self):
        file_path = 'static/data/comments.csv'
        with open(file_path, "r") as csv_file:
            data = list(csv.DictReader(csv_file, delimiter=","))
            for row in data:
                review, _ = Review.objects.get_or_create(pk=row['review_id'])
                author = CustomUser.objects.get(pk=row['author'])
                Comment.objects.create(
                    review_id=review.id,
                    text=row['text'],
                    author_id=author.id,
                    pub_date=row['pub_date']
                )

    def genre_title_load(self):
        file_path = 'static/data/genre_title.csv'
        with open(file_path, "r") as csv_file:
            data = list(csv.DictReader(csv_file, delimiter=","))
            for row in data:
                title, _ = Title.objects.get_or_create(pk=row['title_id'])
                genre = Genre.objects.get(pk=row['genre_id'])
                Genre_Title.objects.create(
                    title_id=title.id,
                    genre_id=genre.id,
                )

    def handle(self, *args, **options):
        Category.objects.all().delete()  # Удалять старые записи стоит только если мы явно хотим это сделать, передав какой-то специальный параметр в команду.
        Title.objects.all().delete()
        Genre.objects.all().delete()
        Review.objects.all().delete()
        self.categories_load()
        self.genres_load()
        self.users_load()
        self.titles_load()
        self.reviews_load()
        self.comments_load()
        self.genre_title_load()  # Надо переписать на bulk_create все, что можно. Оптимизируем загрузку

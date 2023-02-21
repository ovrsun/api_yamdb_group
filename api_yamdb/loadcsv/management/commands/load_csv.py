import csv
from django.core.management import BaseCommand
from reviews.models import Category, Comment, Genre, Title
from users.models import CustomUser


class Command(BaseCommand):
    help = 'description'

    def categories_load(self):
        file_path = 'static/data/category.csv'
        with open(file_path, "r") as csv_file:
            data = list(csv.reader(csv_file, delimiter=","))
            for row in data[1:]:
                Category.objects.create(name=row[1], slug=row[2])

    def genres_load(self):
        file_path = 'static/data/genre.csv'
        with open(file_path, "r") as csv_file:
            data = list(csv.DictReader(csv_file, delimiter=","))
            for row in data[1:]:
                Genre.objects.create(name=row['name'], slug=row['slug'])

    def users_load(self):
        file_path = 'static/data/users.csv'
        with open(file_path, "r") as csv_file:
            data = list(csv.DictReader(csv_file, delimiter=","))
            for row in data[1:]:
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
            for row in data[1:]:
                try:
                    # category, _ = Category.objects.get_or_create(pk=row['category'])
                    category = Category.objects.get(pk=row['category'])
                    Title.objects.create(
                        name=row['name'],
                        year=row['year'],
                        category_id=category.id
                    )
                except Category.DoesNotExist as e:
                    print(e)

    def handle(self, *args, **options):
        self.categories_load()
        # self.genres_load()
        # self.users_load()
        self.titles_load()

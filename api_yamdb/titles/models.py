from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=256, null=False)
    slug = models.SlugField(unique=True, null=False)

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(max_length=256, null=False)
    slug = models.SlugField(unique=True, null=False)

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.CharField(max_length=256)
    category = models.ForeignKey(Category, related_name='titles',
                                 on_delete=models.SET_NULL, null=True)
    genre = models.ManyToManyField(Genre, related_name='titles', null=True)
    description = models.TextField()
    year = models.DateField()

    def __str__(self):
        return self.name

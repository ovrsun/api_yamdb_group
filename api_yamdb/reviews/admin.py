from django.contrib import admin

from .models import Category, Genre, Review, Title, Comment


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'slug')


class ReviewAdmin(admin.ModelAdmin):
    list_display = ('pk', 'text')


class TitleAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'year', 'category')


admin.site.register(Category, CategoryAdmin)
admin.site.register(Genre)
admin.site.register(Comment)
admin.site.register(Title, TitleAdmin)
admin.site.register(Review, ReviewAdmin)

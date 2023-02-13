from django.contrib import admin

from .models import User


class AdminUser(admin.ModelAdmin):
    list_display = ('id', 'username', 'email', 
                    'first_name', 'last_name', 'bio', 'role')
    search_fields = ('username', 'email')

admin.site.register(User, AdminUser)

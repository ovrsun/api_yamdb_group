from django.contrib import admin

from .models import CustomUser


class AdminUser(admin.ModelAdmin):
    list_display = ('username', 'email',
                    'first_name', 'last_name', 'bio', 'role')
    search_fields = ('username', 'email')


admin.site.register(CustomUser, AdminUser)

from django.contrib.auth.models import AbstractUser
from django.db import models


USER = 'user'
MODERATOR = 'moderator'
ADMIN = 'admin'
ROLES = (
    (USER, 'user'),
    (MODERATOR, 'moderator'),
    (ADMIN, 'admin'),
)
class CustomUser(AbstractUser):
    username = models.CharField(
        'Имя пользователя',
        max_length=30,
        unique=True,
    )
    email = models.EmailField(
        'Почта',
        max_length=50,
        unique=True,
    )
    first_name = models.CharField('Имя', max_length=30, blank=True)
    last_name = models.CharField('Фамилия', max_length=30, blank=True)
    bio = models.TextField(
        'Биография',
        blank=True
    )
    role = models.CharField(
        'Роль пользователя',
        max_length=30,
        choices=ROLES,
        default=USER
    )
    confirmation_code = models.CharField(
        'Код',
        max_length=6,
        default='100000'
    )

    @property
    def is_moderator(self):
        return self.role == 'moderator'

    @property
    def is_admin(self):
        return self.role == 'admin'
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator


class Review(models.Model):
    """Модель отзывов к произведениям"""
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Произведения',
        )
    text = models.TextField(max_length=300)
    author = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='автор',
        )
    score = models.IntegerField(
        verbose_name='Оценка отзыва',
        validators=(
            MinValueValidator(1),
            MaxValueValidator(10),
            )
        )
    pub_date = models.DateTimeField(
        verbose_name='Дата публикации',
        auto_now_add=True,
        db_index=True,
    )

    class Meta:
        ordering = ['-pub_date']

    def __str__(self):
        return self.text


class Comment(models.Model):
    """Модель для коменнтариев"""
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Отзыв',
    )
    text = models.CharField(
        max_length=200,
        verbose_name='Тест коментария',
    )
    author = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='автор комента',
    )
    pub_date = models.DateTimeField(
        verbose_name='Дата публикации',
        auto_now_add=True,
        db_index=True,
    )

    class Meta:
        ordering = ['-pub_date']

    def __str__(self):
        return self.text

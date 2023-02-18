from django.urls import include, path
from rest_framework import routers
# from .views import (b, a)
from .views import CategoryViewSet, GenreViewSet, TitleViewSet


app_name = 'api'


router = routers.DefaultRouter()
router.register('titles', TitleViewSet)
router.register('categories', CategoryViewSet)
router.register('genres', GenreViewSet)

urlpatterns = [
    path('', include(router.urls)),
    # path('auth/signup/', a.as_view()),
    # path('auth/token/', b.as_view()),
]

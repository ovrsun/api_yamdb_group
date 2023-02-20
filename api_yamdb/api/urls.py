from django.urls import include, path
from rest_framework import routers
# from .views import (b, a)
from .views import CategoryViewSet, GenreViewSet, TitleViewSet


app_name = 'api'


router_v1 = routers.DefaultRouter()
router_v1.register('titles', TitleViewSet)
router_v1.register('categories', CategoryViewSet)
router_v1.register('genres', GenreViewSet)

urlpatterns = [
    path('', include(router_v1.urls)),
    # path('auth/signup/', a.as_view()),
    # path('auth/token/', b.as_view()),
]

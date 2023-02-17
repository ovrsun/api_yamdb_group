from django.urls import include, path
from rest_framework import routers

from .views import ReviewViewSet, CommentViewSet
app_name = 'api'

v1_router = routers.DefaultRouter()
v1_router.register(
    r'^title/(?P<title_id>\d+)/reviews', ReviewViewSet, basename='reviews')
v1_router.register(
    r'^titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet, basename='comments')

urlpatterns = [
    path('v1/', include(v1_router.urls)),
]

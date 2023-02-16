from django.urls import include, path
from rest_framework import routers
from .views import (b, a)


router = routers.DefaultRouter()
urlpatterns = [
    path('api/v1/', include(router.urls)),
    path('api/v1/auth/signup/', a.as_view()),
    path('api/v1/auth/token/', b.as_view()),
]
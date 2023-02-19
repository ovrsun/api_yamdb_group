from django.urls import include, path
from rest_framework import routers

from users.views import GetToken, UserViewSet, signup

app_name = 'api'

router = routers.DefaultRouter()
router.register('users', UserViewSet, basename='users')

urlpatterns = [
    path('v1/', include(router.urls)),
    path('v1/auth/signup/', signup, name='signup'),
    path('v1/auth/token/', GetToken.as_view()),
]

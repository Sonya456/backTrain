from django.urls import path, include, re_path
from rest_framework.routers import DefaultRouter

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .viewsets import TopicViewSet, AnswerViewSet, QuestionViewSet, UserTopicViewSet, AnswerUserViewSet, QuestionUserViewSet, UserWordViewSet

router = DefaultRouter()
router.register(r'answers', AnswerViewSet)
router.register(r'user-answers', AnswerUserViewSet)

router.register(r'questions', QuestionViewSet)
router.register(r'user-questions', QuestionUserViewSet)

router.register(r'topics', TopicViewSet)
router.register(r'user-topics', UserTopicViewSet, basename='user-topic')

router.register(r'words', UserWordViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('login/', include('rest_framework.urls')),
    path('auth/', include('djoser.urls')),
    re_path(r'^auth/', include('djoser.urls.authtoken')),
]

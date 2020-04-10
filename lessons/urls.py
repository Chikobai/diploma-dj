from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import LessonViewSet, QuestionAnswersViewSet

router = DefaultRouter()
router.register(r'course/modules/(?P<module_id>.+)/lessons', LessonViewSet, "lessons")
router.register(r'question', QuestionAnswersViewSet, "questions_")

urlpatterns = [
    path('', include(router.urls)),
]

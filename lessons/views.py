from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework import permissions
from rest_framework.response import Response

from .models import Lesson, Question, Answer, LessonTaker
from .serializers import LessonSerializer


class LessonViewSet(viewsets.ModelViewSet):
    serializer_class = LessonSerializer
    permission_classes = [permissions.IsAuthenticated]
    http_method_names = ['get']

    def get_queryset(self):
        id = self.kwargs['module_id']
        querysets = Lesson.objects.filter(module=id)
        return querysets


class QuestionAnswersViewSet(viewsets.ViewSet):

    @action(detail=False, methods=['post'], permission_classes=[permissions.AllowAny])
    def reply(self, request):
        user = request.user
        data = request.data
        lesson_id = data.get('lesson', None)
        question_id = data.get('question', None)
        answer_id = data.get('answer', None)

        if lesson_id is None:
            return self.get_response_data(False, 'lesson объязательное поле', status.HTTP_400_BAD_REQUEST)

        if question_id is None:
            return self.get_response_data(False, 'question объязательное поле', status.HTTP_400_BAD_REQUEST)

        if answer_id is None:
            return self.get_response_data(False, 'answer объязательное поле', status.HTTP_400_BAD_REQUEST)

        try:
            lesson = Lesson.objects.get(pk=lesson_id)
        except Lesson.DoesNotExist:
            lesson = None

        try:
            question = Question.objects.get(pk=question_id)
        except Question.DoesNotExist:
            question = None

        try:
            answer = Answer.objects.get(pk=answer_id)
        except Answer.DoesNotExist:
            answer = None

        if lesson is None:
            return self.get_response_data(False, 'Не найден такой урок', status.HTTP_400_BAD_REQUEST)

        if question is None:
            return self.get_response_data(False, 'Не найден такой вопрос', status.HTTP_400_BAD_REQUEST)

        if answer is None:
            return self.get_response_data(False, 'Не найден такой ответ', status.HTTP_400_BAD_REQUEST)

        if question.lesson != lesson:
            return self.get_response_data(False, 'Вопрос не соответсвует к уроку', status.HTTP_400_BAD_REQUEST)

        if answer.question != question:
            return self.get_response_data(False, 'Ответ не соответсвует к вопросу', status.HTTP_400_BAD_REQUEST)

        taker, created = LessonTaker.objects.get_or_create(user=user, lesson=lesson)

        if answer.is_true:
            asd = taker.correct_answers+1
            taker.correct_answers = asd
            taker.save()
            return self.get_response_data(True, 'Првильный ответ', status.HTTP_200_OK)
        else:
            return self.get_response_data(False, 'Неверный ответ', status.HTTP_200_OK)

    def get_response_data(self, _success, _message, _status):
        response_data = dict()
        response_data['success'] = _success
        response_data['message'] = _message
        return Response(response_data, status=_status)



import time

from courses.models import Course
from rest_framework import viewsets, status, permissions
from rest_framework.response import Response
from users.models import User

from .models import Review
from .serializers import ReviewSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticated,]
    http_method_names = ['get', 'post']

    def get_queryset(self):
        course_id = self.kwargs['course_id']
        queryset = Review.objects.filter(course=course_id)
        return queryset

    def create(self, request, *args, **kwargs):
        course_id = self.kwargs['course_id']
        reviewer = request.user
        text = request.data['text']
        rating = request.data['rating']

        try:
            course = Course.objects.get(id=course_id)
        except Course.DoesNotExist:
            response_data = {
                'detail': 'Сourse с такими id не найден'
            }
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)

        review, created = Review.objects.update_or_create(reviewer=reviewer, course=course, defaults={'text': text,
                                                                                                      'rating': rating})
        reviewer_data = {
            'id': reviewer.id,
            'email': reviewer.email,
            'first_name': reviewer.first_name,
            'last_name': reviewer.last_name
        }
        created_in_sec = int(time.mktime(review.created.timetuple()))
        response_data = {
            'id': review.pk,
            'text': review.text,
            'rating': review.rating,
            'created': review.created,
            'created_in_sec': created_in_sec,
            'reviewer': reviewer_data
        }
        if created:
            return Response(response_data, status=status.HTTP_201_CREATED)
        else:
            return Response(response_data, status=status.HTTP_200_OK)

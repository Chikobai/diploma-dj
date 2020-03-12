from rest_framework import viewsets, permissions
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse

from .models import Post
from posts.permissions import IsOwnerOrReadOnly
from posts.serializers import PostSerializer


@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'deliveries': reverse('deliveries-list', request=request, format=format)
    })


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated,
                          IsOwnerOrReadOnly]
    http_method_names = ['get']

    def retrieve(self, request, *args, **kwargs):
        delivery = self.get_object()
        delivery.viewed = delivery.viewed + 1
        delivery.save()
        serializer = self.get_serializer(delivery)
        return Response(serializer.data)

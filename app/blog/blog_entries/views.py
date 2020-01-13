from rest_framework import status

from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from blog_auth.models import User
from .models import Article 
from .permissions import IsOwnerOrSuperUserOrReadOnly
from .serializers import ArticleSerializer

class ArticleViewSet(ModelViewSet):
    serializer_class = ArticleSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrSuperUserOrReadOnly]
    queryset = Article.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = User.objects.get(user_authenticate_data=request.user)
        instance_article = serializer.save()
        instance_article.author = user
        instance_article.save()
        return Response(
            data=serializer.data,
            status=status.HTTP_201_CREATED
        )
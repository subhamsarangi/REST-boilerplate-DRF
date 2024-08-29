from rest_framework.response import Response
from rest_framework import generics, permissions, status
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated

from .models import Article
from .serializers import ArticleSerializer



class ArticleListCreateView(generics.ListCreateAPIView):
    serializer_class = ArticleSerializer
    permission_classes = [permissions.AllowAny]  # Allow anyone to list published articles

    def get_queryset(self):
        if self.request.method == 'GET':
            return Article.objects.filter(is_published=True)
        return Article.objects.all()

    def perform_create(self, serializer):
        # Set the owner to the current user
        if self.request.user and not self.request.user.is_anonymous:
            serializer.save(owner=self.request.user)
        else:
            raise permissions.PermissionDenied("User must be authenticated to create an article.")


class UserPublishedArticleListView(generics.ListAPIView):
    serializer_class = ArticleSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Article.objects.filter(is_published=True, owner=user)


class UserPrivateArticleListView(generics.ListAPIView):
    serializer_class = ArticleSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Article.objects.filter(is_published=False, owner=user)


class ArticleRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ArticleSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        """
            Ensure that the article is either published or owned by the current user.
        """
        user = self.request.user
        published_articles = Article.objects.filter(id=self.kwargs['pk'], is_published=True)
        owned_articles = Article.objects.filter(id=self.kwargs['pk'], owner=user)

        return published_articles | owned_articles

    def perform_update(self, serializer):
        user = self.request.user
        article = self.get_object()
        if article.owner != user:
            raise permissions.PermissionDenied("You do not have permission to edit this article.")
        serializer.save(owner=user)

    def delete(self, request, *args, **kwargs):
        article = self.get_object()
        if article.owner != request.user:
            raise permissions.PermissionDenied("You do not have permission to delete this article.")
        super().delete(request, *args, **kwargs)
        return Response({'detail': 'Article successfully deleted'}, status=status.HTTP_204_NO_CONTENT)

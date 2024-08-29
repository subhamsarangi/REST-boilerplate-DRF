from rest_framework import generics, permissions
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
        return Article.objects.filter(id=self.kwargs['pk'], is_published=True) | Article.objects.filter(id=self.kwargs['pk'], owner=user)

    def perform_update(self, serializer):
        serializer.save(owner=self.request.user)

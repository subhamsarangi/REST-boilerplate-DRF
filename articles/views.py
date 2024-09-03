from rest_framework.pagination import PageNumberPagination
from rest_framework.generics import ListCreateAPIView, ListAPIView
from rest_framework.permissions import AllowAny, IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from rest_framework.viewsets import ModelViewSet

from .models import Article
from .serializers import ArticleSerializer
from .mixins import ArticlePermissionMixin
from .tasks import basic_article_task


class ArticleListCreateView(ListCreateAPIView):
    serializer_class = ArticleSerializer
    permission_classes = [AllowAny]  # Allow anyone to list published articles
    pagination_class = PageNumberPagination

    def get_queryset(self):
        if self.request.method == 'GET':
            return Article.objects.filter(is_published=True)
        return Article.objects.all()

    def perform_create(self, serializer):
        # Set the owner to the current user
        if self.request.user and not self.request.user.is_anonymous:
            serializer.save(owner=self.request.user)
        else:
            raise PermissionDenied("User must be authenticated to create an article.")


class UserPublishedArticleListView(ListAPIView):
    serializer_class = ArticleSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = PageNumberPagination

    def get_queryset(self):
        user = self.request.user
        return Article.objects.filter(is_published=True, owner=user)


class UserPrivateArticleListView(ListAPIView):
    serializer_class = ArticleSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = PageNumberPagination

    def get_queryset(self):
        user = self.request.user
        return Article.objects.filter(is_published=False, owner=user)


# Filtering Across All Methods: If you want to apply the same filter across all methods in your view
# (list, retrieve, update, delete), get_queryset is a good place to centralize this logic.

class ArticleViewSet(ArticlePermissionMixin, ModelViewSet):
    serializer_class = ArticleSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    lookup_field = 'slug'

    def get_queryset(self):
        basic_article_task.delay("aws certifications", "reactjs concepts")
        return Article.objects.all()

    def get_object(self):
        article = super().get_object()
        self.check_article_permissions(article, self.action)
        return article

    def perform_update(self, serializer):
        serializer.save(owner=self.request.user)

    def perform_destroy(self, instance):
        super().perform_destroy(instance)

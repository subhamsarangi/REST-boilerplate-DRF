from rest_framework import status
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework.generics import ListCreateAPIView, ListAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import AllowAny, IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.exceptions import PermissionDenied, NotFound

from .models import Article
from .serializers import ArticleSerializer


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


class ArticleRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    serializer_class = ArticleSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    # Filtering Across All Methods: If you want to apply the same filter across all methods in your view
    # (list, retrieve, update, delete), get_queryset is a good place to centralize this logic.

    def get_object(self):
        slug = self.kwargs.get('slug')
        try:
            return Article.objects.get(slug=slug)
        except Article.DoesNotExist:
            raise NotFound("Article not found")

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.owner != request.user and not instance.is_published:
            raise PermissionDenied("You do not have permission to view this article.")
        return Response({
            'detail': 'Article successfully fetched',
            'data': self.get_serializer(instance).data
        })

    def perform_update(self, serializer): # pre-delete update
        article = self.get_object()
        user = self.request.user
        if article.owner != user:
            raise PermissionDenied("You do not have permission to edit this article.")
        serializer.save(owner=user)
    
    def update(self, request, *args, **kwargs):
        super().update(request, *args, **kwargs)
        return Response({'detail': 'Article successfully updated'}, status=status.HTTP_200_OK)

    def perform_destroy(self, instance): # pre-delete logic
        instance = self.get_object()
        if instance.owner != self.request.user:
            raise PermissionDenied("You do not have permission to delete this article.")
        instance.delete()

    def delete(self, request, *args, **kwargs):
        super().delete(request, *args, **kwargs)
        return Response({'detail': 'Article successfully deleted'}, status=status.HTTP_204_NO_CONTENT)

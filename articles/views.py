from django.contrib.postgres.search import SearchQuery, SearchVector, TrigramSimilarity, SearchRank
from rest_framework.pagination import PageNumberPagination
from rest_framework.generics import ListCreateAPIView, ListAPIView
from rest_framework.permissions import AllowAny, IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from rest_framework.viewsets import ModelViewSet
from django.db.models import F, Q
from django.http import JsonResponse
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

from .models import Article
from .serializers import ArticleSerializer
from .mixins import ArticlePermissionMixin
from .tasks import increment_article_view_count


class ArticleListCreateView(ListCreateAPIView):
    serializer_class = ArticleSerializer
    permission_classes = [AllowAny]  # Allow anyone to list published articles
    pagination_class = PageNumberPagination

    def get_queryset(self):
        if self.request.method == 'GET':
            queryset = Article.objects.filter(is_published=True)
            query = self.request.query_params.get('search', None)
            if query:                
                search_vector = SearchVector('title', 'content')
                search_query = SearchQuery(query)
                queryset = queryset.annotate(
                    rank=SearchRank(search_vector, search_query),
                    title_similarity=TrigramSimilarity('title', query),
                    content_similarity=TrigramSimilarity('content', query)
                ).filter(
                    Q(rank__gt=0.1) | Q(title_similarity__gt=0.3) | Q(content_similarity__gt=0.3)
                ).order_by('-rank', '-title_similarity', '-content_similarity')
                # queryset = queryset.annotate(search=search_vector).filter(search=search_query)
            return queryset
        return Article.objects.all()

    def perform_create(self, serializer):
        # Set the owner to the current user
        if self.request.user and not self.request.user.is_anonymous:
            serializer.save(owner=self.request.user)
        else:
            raise PermissionDenied("User must be authenticated to create an article.")


# Filtering Across All Methods: If you want to apply the same filter across all methods in your view
# (list, retrieve, update, delete), get_queryset is a good place to centralize this logic.

class ArticleViewSet(ArticlePermissionMixin, ModelViewSet):
    serializer_class = ArticleSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    lookup_field = 'slug'

    def get_queryset(self):
        queryset = Article.objects.all()
        return queryset

    def get_object(self):
        article = super().get_object()
        self.check_article_permissions(article, self.action)
        task = increment_article_view_count.delay(article.slug)
        print(task.id, "-------------------------------<.")
        return article

    def perform_update(self, serializer):
        serializer.save(owner=self.request.user)

    def perform_destroy(self, instance):
        super().perform_destroy(instance)


class UserPublishedArticleListView(ListAPIView):
    serializer_class = ArticleSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = PageNumberPagination

    def get_queryset(self):
        user = self.request.user
        queryset = Article.objects.filter(is_published=True, owner=user)
        search_query = self.request.query_params.get('search', None)
        if search_query:
            search_vector = SearchVector('title', 'content')
            search_query = SearchQuery(search_query)
            queryset = queryset.annotate(search=search_vector).filter(search=search_query)
        return queryset


class UserPrivateArticleListView(ListAPIView):
    serializer_class = ArticleSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = PageNumberPagination

    def get_queryset(self):
        user = self.request.user
        queryset = Article.objects.filter(is_published=False, owner=user)
        search_query = self.request.query_params.get('search', None)
        if search_query:
            search_vector = SearchVector('title', 'content')
            search_query = SearchQuery(search_query)
            queryset = queryset.annotate(search=search_vector).filter(search=search_query)
        return queryset


def send_message(request):
    message = request.POST.get('message', 'Default message')
    group_name = 'some_room_name'  # Ensure this matches the group in your consumer

    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        group_name,
        {
            'type': 'chat_message',
            'message': message
        }
    )

    return JsonResponse({'status': 'Message sent'})
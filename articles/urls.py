from django.urls import path, include
from rest_framework.routers import SimpleRouter

from . import views


router = SimpleRouter()
router.register(r'articles', views.ArticleViewSet, basename='article')

urlpatterns = [
    path('articles/', views.ArticleListCreateView.as_view(), name='article_list_create'),
    path('articles/user/published/', views.UserPublishedArticleListView.as_view(), name='user_published_articles'),
    path('articles/user/private/', views.UserPrivateArticleListView.as_view(), name='user_private_articles'),
    # path('articles/<slug:slug>/', views.ArticleRetrieveUpdateDestroyView.as_view(), name='article-detail-update-delete'),
    path('', include(router.urls)),
]

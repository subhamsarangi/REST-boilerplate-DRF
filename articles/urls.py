from django.urls import path
from . import views

urlpatterns = [
    path('articles/', views.ArticleListCreateView.as_view(), name='article_list_create'),
    path('articles/user/published/', views.UserPublishedArticleListView.as_view(), name='user_published_articles'),
    path('articles/user/private/', views.UserPrivateArticleListView.as_view(), name='user_private_articles'),
    path('articles/<int:pk>/', views.ArticleRetrieveUpdateDestroyView.as_view(), name='article-detail-update-delete'),
]

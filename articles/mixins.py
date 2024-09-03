from rest_framework.exceptions import PermissionDenied

class ArticlePermissionMixin:
    def check_article_permissions(self, article, action):
        user = self.request.user
        if action == 'retrieve' and article.owner != user and not article.is_published:
            raise PermissionDenied("You do not have permission to view this article.")
        if action in ['update', 'destroy'] and article.owner != user:
            raise PermissionDenied(f"You do not have permission to {action} this article.")

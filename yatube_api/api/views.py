from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, mixins, permissions, viewsets

from posts.models import Group, Post
from .pagination import CustomPagination
from .permissions import IsAuthorOrReadOnly
from .serializers import (CommentSerializer, FollowSerializer,
                          GroupSerializer, PostSerializer)


class ListCreateViewSet(mixins.CreateModelMixin, mixins.ListModelMixin,
                        viewsets.GenericViewSet):
    pass


class FollowViewSet(ListCreateViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = FollowSerializer
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    search_fields = ('following__username',)

    def get_queryset(self):
        user = self.request.user
        return user.follows.all()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class PostViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, ]
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    pagination_class = CustomPagination

    def get_permissions(self):
        if self.action == 'create' or 'put' or 'patch' or 'delete':
            return (IsAuthorOrReadOnly(),)
        return super().get_permissions()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, ]
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class CommentViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, ]
    serializer_class = CommentSerializer

    def get_permissions(self):
        if self.action == 'patch' or 'delete':
            return (IsAuthorOrReadOnly(),)
        return super().get_permissions()

    def get_queryset(self):
        post_id = self.kwargs.get("post_id")
        post = get_object_or_404(Post, id=post_id)
        return post.comments.all()

    def perform_create(self, serializer):
        post_id = self.kwargs.get("post_id")
        post = get_object_or_404(Post, id=post_id)
        serializer.save(author=self.request.user, post=post)

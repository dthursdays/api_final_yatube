from django.contrib.auth import get_user_model
from posts.models import Comment, Follow, Group, Post
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

User = get_user_model()


class FollowSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True, default=serializers.CurrentUserDefault())

    following = serializers.SlugRelatedField(
        slug_field='username',
        read_only=False,
        queryset=User.objects.all())

    class Meta:
        fields = "__all__"
        model = Follow
        validators = [
            UniqueTogetherValidator(
                queryset=Follow.objects.all(),
                fields=('user', 'following')
            )
        ]

    def validate(self, data):
        if self.context.get('request').user == data['following']:
            raise serializers.ValidationError(
                'You can\'t follow yourself!')
        return data


class PostSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True, default=serializers.CurrentUserDefault())

    class Meta:
        fields = "__all__"
        model = Post


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        fields = "__all__"
        model = Group


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True, default=serializers.CurrentUserDefault())

    post = serializers.PrimaryKeyRelatedField(
        read_only=True)

    class Meta:
        fields = "__all__"
        model = Comment

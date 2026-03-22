from rest_framework import serializers

from .models import Post, Comment, Category, User


class PostListSerializer(serializers.ModelSerializer):
    author_username = serializers.CharField(
        source="author.username", 
        read_only=True
    )
    author_profile_photo = serializers.ImageField(
        source="author.profile.profile_photo", 
        read_only=True
    )
    category_name = serializers.CharField(
        source="category.name", 
        read_only=True
    )
    comments_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Post
        fields = [
            "id",
            "title",
            "author_username",
            "author_profile_photo",
            "category_name",
            "created_at",
            "comments_count"
        ]


class AuthorSerializer(serializers.ModelSerializer):
    profile_photo = serializers.ImageField(
        source="profile.profile_photo", 
        read_only=True
    )

    class Meta:
        model = User
        fields = [
            "id", 
            "username", 
            "profile_photo"
        ]


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name"]


class CommentSerializer(serializers.ModelSerializer):
    author_username = serializers.CharField(
        source="author.username", 
        read_only=True
    )

    class Meta:
        model = Comment
        fields = [
            "id", 
            "author_username", 
            "text", 
            "created_at"
        ]


class PostDetailSerializer(serializers.ModelSerializer):
    author = AuthorSerializer(read_only=True)
    category = CategorySerializer(read_only=True)
    comments = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = Post
        fields = [
            "id",
            "title",
            "content",
            "author",
            "category",
            "created_at",
            "is_published",
            "comments",
        ]


class PostCreateSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Post
        fields = [
            "id",
            "title", 
            "content", 
            "category", 
            "is_published"
        ]

from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from django.shortcuts import get_object_or_404
from django.db.models import Q, Count
from drf_yasg.utils import swagger_auto_schema

from .models import Post
from .serializers import (
    PostListSerializer, 
    PostCreateSerializer, 
    PostDetailSerializer, 
    CommentSerializer
)
from .paginations import CustomPageNumberPaginator


class PostListCreateAPIView(APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        post_list = Post.objects.filter(is_published=True)

        post_list = post_list.select_related(
            "author",
            "author__profile",
            "category",
        ).prefetch_related(
            "comments"
        ).annotate(
            comments_count=Count("comments")
        )

        category = self.request.query_params.get("category")
        author = self.request.query_params.get("author")
        search = self.request.query_params.get("search")
        ordering = self.request.query_params.get("ordering")

        if category:
            post_list = post_list.filter(category_id=category)

        if author:
            post_list = post_list.filter(author_id=author)

        if search:
            post_list = post_list.filter(
                Q(title__icontains=search) |
                Q(content__icontains=search)
            )

        if ordering:
            post_list = post_list.order_by(ordering)

        return post_list

    def get(self, request):
        posts = self.get_queryset()

        paginator = CustomPageNumberPaginator()
        paginated_queryset = paginator.paginate_queryset(posts, request)
        
        serializer = PostListSerializer(paginated_queryset, many=True)
        return paginator.get_paginated_response(serializer.data)

    @swagger_auto_schema(request_body=PostCreateSerializer)
    def post(self, request):
        serializer = PostCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(author=request.user)
            return Response(
                serializer.data, 
                status=status.HTTP_201_CREATED
            )
        return Response(
            serializer.errors, 
            status=status.HTTP_400_BAD_REQUEST
        )


class PostDetailAPIView(APIView):
    def get_object(self, pk):
        return get_object_or_404(Post, pk=pk)
    
    def get(self, request, pk):
        post = self.get_object(pk)
        serializer = PostDetailSerializer(post)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CommentCreateAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(request_body=CommentSerializer)
    def post(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        serializer = CommentSerializer(data=request.data)
        
        if serializer.is_valid():
            serializer.save(author=request.user, post=post)
            return Response(
                serializer.data, 
                status=status.HTTP_201_CREATED
            )
        return Response(
            serializer.errors, 
            status=status.HTTP_400_BAD_REQUEST
        )

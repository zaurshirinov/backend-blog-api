from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework.test import APITestCase, APIClient
from rest_framework import status

from blog.models import Post, Category, Comment


class PostAPITest(APITestCase):

    def setUp(self):
        self.client = APIClient()

        self.user = User.objects.create_user(
            username="testuser",
            password="testpass123"
        )

        self.category = Category.objects.create(name="Tech")

        self.post = Post.objects.create(
            author=self.user,
            category=self.category,
            title="Test Post",
            content="Test Content",
            is_published=True
        )

        self.comment = Comment.objects.create(
            post=self.post,
            author=self.user,
            text="Test comment"
        )

        self.list_url = "/api/posts/"
        self.detail_url = f"/api/posts/{self.post.id}/"
        self.comment_url = f"/api/posts/{self.post.id}/comments/"

    def test_post_list_returns_paginated_results(self):
        response = self.client.get(self.list_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("results", response.data)
        
    def test_filter_by_category(self):
        response = self.client.get(self.list_url, {"category": self.category.id})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 1)

    def test_search_works(self):
        response = self.client.get(self.list_url, {"search": "Test"})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 1)

    def test_post_detail_returns_nested_comments(self):
        response = self.client.get(self.detail_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("comments", response.data)
        self.assertEqual(len(response.data["comments"]), 1)

    def test_unauthenticated_user_cannot_create_post(self):
        data = {
            "title": "New Post",
            "content": "New Content",
            "category": self.category.id
        }

        response = self.client.post(self.list_url, data)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_authenticated_user_can_create_post(self):
        self.client.login(username="testuser", password="testpass123")

        data = {
            "title": "New Post",
            "content": "New Content",
            "category": self.category.id
        }

        response = self.client.post(self.list_url, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Post.objects.count(), 2)

    def test_authenticated_user_can_comment(self):
        self.client.login(username="testuser", password="testpass123")

        data = {
            "text": "New Comment"
        }

        response = self.client.post(self.comment_url, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Comment.objects.count(), 2)

    def test_comments_count_is_correct(self):
        response = self.client.get(self.list_url)

        post = response.data["results"][0]

        self.assertEqual(post["comments_count"], 1)

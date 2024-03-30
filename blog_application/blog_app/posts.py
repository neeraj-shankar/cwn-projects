from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from blog_app.serializers import PostSerializer
from rest_framework import status
from blog_app.models import Post
from utils.logger import setup_logger
from django.db import IntegrityError

from django.contrib.auth.models import User



log = setup_logger(__name__)


class PostList(APIView):
    """
    PostList is a DRF APIView that handles CRUD operations for posts.

    Attributes:
        serializer_class (Serializer): The serializer class used for serializing Post objects.

    Methods:
        get(request, format=None): Retrieves a list of posts.
        post(request, format=None): Creates a new post.
        put(request, pk): Updates an existing post.
    """

    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def get_serializer(self, *args, **kwargs):
        """
        Return the serializer instance that should be used for validating and
        deserializing input, and for serializing output.
        """
        if self.request.method == "POST":
            # Use a different serializer for POST requests if needed
            return PostSerializer(*args, **kwargs)
        return super().get_serializer(*args, **kwargs)

    def get(self, request, format=None):
        """
        Get a list of posts.

        Args:
            request (Request): The HTTP request.

        Returns:
            Response: A JSON response with a list of serialized posts.
        """
        post = (
            Post.objects.all().select_related("author").prefetch_related("categories")
        )
        serializer = PostSerializer(post, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, format=None):
        """
        Create a new post.

        Args:
            request (Request): The HTTP request containing post data.

        Returns:
            Response: A JSON response with the serialized post if successful, or errors if unsuccessful.
        """
        try:
            log.info(f"Received Post Data: {request.data}")
            serializer = self.get_serializer(data=request.data)
            log.info(f"Validation Successfully Completed for Post data")
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                log.info(f"Saving to post database Successful")
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except IntegrityError as e:
            log.error(f"Error saving to post database: {e}")
            return Response(
                {"error": "Database error"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class PostDetail(APIView):
    """
    PostDetail is a DRF APIView that handles CRUD operations for posts.

    Attributes:
        serializer_class (Serializer): The serializer class used for serializing Post objects.

    Methods:
        get_post(self, pk, format=None): Retrieves post if that exists else raise not found response
        get(request, pk, format=None): Retrieves specific post based on given pk.
        put(request, pk): Updates an existing post.
    """

    def get_post(self, pk, format=None):
        try:
            # Returns the retrieves post object
            return Post.objects.get(pk=pk)
        except Post.DoesNotExist:
            raise Response(
                {"error": "Post not found"}, status=status.HTTP_404_NOT_FOUND
            )

    def get(self, request, pk):
        post = self.get_post(pk)
        serializer = PostSerializer(post)
        return Response(serializer.data)

    def put(self, request, pk):
        """
        Update an existing post.

        Args:
            request (Request): The HTTP request containing updated post data.
            pk (int): The primary key of the post to be updated.

        Returns:
            Response: A JSON response with the updated serialized post if successful, or errors if unsuccessful.
        """
        post = self.get_post(pk)
        if not post:
            return Response(
                {"error": "Post not found"}, status=status.HTTP_404_NOT_FOUND
            )
        
        serializer = PostSerializer(post, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, format=None):
        """
        Delete one or more posts.

        Args:
            request (Request): The HTTP request.

        Returns:
            Response: A JSON response indicating the success of the delete operation.
        """
        pk = request.data.get("pk", [])
        log.info(f"Received IDS for deletion: {pk}")
        if not pk:
            return Response(
                {"error": "Please provide one or more primary keys for deletion"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        posts = Post.objects.filter(pk__in=pk)

        if not posts.exists():
            return Response(
                {"error": "No posts found with the provided primary keys"},
                status=status.HTTP_404_NOT_FOUND,
            )

        posts.delete()
        return Response(
            {"message": "Posts deleted successfully"}, status=status.HTTP_204_NO_CONTENT
        )

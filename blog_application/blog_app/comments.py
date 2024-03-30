from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from blog_app.serializers import CommentSerializer
from rest_framework import status
from blog_app.models import Comment
from utils.logger import setup_logger
from django.db import IntegrityError
from rest_framework.exceptions import APIException


from django.contrib.auth.models import User


log = setup_logger(__name__)


class CommentList(APIView):
    """
    CommentList is a DRF APIView that handles CRUD operations for comments.

    Attributes:
        serializer_class (Serializer): The serializer class used for serializing Comment objects.

    Methods:
        get(request, format=None): Retrieves a list of comments.
        post(request, format=None): Creates a new comment.
        put(request, pk): Updates an existing comment.
    """

    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def get_serializer(self, *args, **kwargs):
        """
        Return the serializer instance that should be used for validating and
        deserializing input, and for serializing output.
        """
        if self.request.method == "POST":
            # Use a different serializer for POST requests if needed
            return CommentSerializer(*args, **kwargs)
        return super().get_serializer(*args, **kwargs)

    def get(self, request, format=None):
        """
        Get a list of comments.

        Args:
            request (Request): The HTTP request.

        Returns:
            Response: A JSON response with a list of serialized comments.
        """
        post = Comment.objects.all().select_related("author").select_related("post")
        serializer = CommentSerializer(post, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, format=None):
        """
        Create a new comment.

        Args:
            request (Request): The HTTP request containing cooment data.

        Returns:
            Response: A JSON response with the serialized cooment if successful, or errors if unsuccessful.
        """
        try:
            log.info(f"Received Comment Data: {request.data}")
            serializer = self.get_serializer(data=request.data)
            log.info(f"Validation Successfully Completed for Comment data")
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                log.info(f"Saving to Comment database Successful")
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except IntegrityError as e:
            log.error(f"Error saving to comment database: {e}")
            return Response(
                {"error": "Database error"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class CommentDetail(APIView):
    """
    CommentDetail is a DRF APIView that handles CRUD operations for comments.

    Attributes:
        serializer_class (Serializer): The serializer class used for serializing Comment objects.

    Methods:
        get_post(self, pk, format=None): Retrieves post if that exists else raise not found response
        get(request, pk, format=None): Retrieves specific comment based on given pk.
        put(request, pk): Updates an existing post.
    """

    def get_comment(self, pk, format=None):
        try:
            return Comment.objects.get(pk=pk)
        except Comment.DoesNotExist as e:
            not_found = {"error": "Requested Comment does not exist."}
            return Response(not_found, status=status.HTTP_404_NOT_FOUND)

    def get(self, request, pk):
        comment = self.get_post(pk)
        serializer = CommentSerializer(comment)
        return Response(serializer.data)

    def put(self, request, pk):
        """
        Update an existing comment.

        Args:
            request (Request): The HTTP request containing updated comment data.
            pk (int): The primary key of the comment to be updated.

        Returns:
            Response: A JSON response with the updated serialized post if successful, or errors if unsuccessful.
        """
        comment = self.get_comment(pk)
        serializer = CommentSerializer(comment, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, format=None):
        """
        Delete one or more comments.

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

        posts = Comment.objects.filter(pk__in=pk)

        if not posts.exists():
            return Response(
                {"error": "No comments found with the provided primary keys"},
                status=status.HTTP_404_NOT_FOUND,
            )

        posts.delete()
        return Response(
            {"message": "Comments deleted successfully"},
            status=status.HTTP_204_NO_CONTENT,
        )

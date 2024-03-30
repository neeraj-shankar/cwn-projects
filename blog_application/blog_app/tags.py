from django.shortcuts import get_object_or_404
from blog_app.models import Tag
from blog_app.serializers import TagSerializer
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from utils.logger import setup_logger

log = setup_logger(__name__)


class TagViewSet(viewsets.ViewSet):

    def list(self, request):

        queryset = Tag.objects.all()
        serializer = TagSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset = Tag.objects.all()
        tag = get_object_or_404(queryset, pk=pk)
        serializer = TagSerializer(tag)
        return Response(serializer.data)

    def create(self, request):
        """
        Handles POST request to create a new Category Model Instance
        """
        log.info(f"Request Data: {request.data}")
        log.info(f"Request Data Type: {type(request.data)}")
        serializer = TagSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, pk=None):
        """
        Handles PATCH request to partially Update Category Instance
        """
        log.info(f"primary key: {pk}")
        tag = Tag.objects.get(id=pk)
        serializer = TagSerializer(tag, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def destroy(self, request, pk=None):
        queryset = Tag.objects.all()
        tag = get_object_or_404(queryset, pk=pk)
        tag.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


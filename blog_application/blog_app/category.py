from django.shortcuts import get_object_or_404
from blog_app.models import Category
from blog_app.serializers import CategorySerializer
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from utils.logger import setup_logger

log = setup_logger(__name__)


class CategoryViewSet(viewsets.ViewSet):

    def list(self, request):

        queryset = Category.objects.all()
        serializer = CategorySerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset = Category.objects.all()
        category = get_object_or_404(queryset, pk=pk)
        serializer = CategorySerializer(category)
        return Response(serializer.data)

    def create(self, request):
        """
        Handles POST request to create a new Category Model Instance
        """
        log.info(f"Request Data: {request.data}")
        log.info(f"Request Data Type: {type(request.data)}")
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, pk=None):
        """
        Handles PATCH request to partially Update Category Instance
        """
        category = Category.objects.get(id=pk)
        serializer = CategorySerializer(category, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def destroy(self, request, pk=None):
        queryset = Category.objects.all()
        category = get_object_or_404(queryset, pk=pk)
        category.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


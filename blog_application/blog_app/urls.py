from django.urls import path
from blog_app import category, posts, comments, tags, likes
from rest_framework.routers import DefaultRouter

urlpatterns = [
    path('post/', posts.PostList.as_view(), name='blog_app__post_list'),
    path('post/<int:pk>/', posts.PostDetail.as_view(), name='blog_app__post_detail'),
    path('posts/delete/', posts.PostDetail.as_view(), name='blog_app__post-delete-multiple'),
    path('comment/', comments.CommentList.as_view(), name='blog_app__comment_list'),
    path('comment/<int:pk>/', comments.CommentDetail.as_view(), name='blog_app__commentt_detail'),
    path('comment/delete/', comments.CommentDetail.as_view(), name='blog_app__comment-delete-multiple'),

    #  URL pattern for the SnippetList view (list and create)
    path('likes/', likes.LikeList.as_view(), name='blog_app__like_list'),

    # URL pattern for the SnippetDetail view (retrieve, update, delete)
    path('likes/<int:pk>/', likes.LikeDetail.as_view(), name='blog_app__like_detail'),

    
]

router = DefaultRouter()
router.register(r'category', category.CategoryViewSet, basename='blog_app-category')
router.register(r'tag', tags.TagViewSet, basename='blog_app-tag')
urlpatterns += router.urls

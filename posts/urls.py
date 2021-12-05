from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import (
    PostViewSet,
    PostCommentCreateView,
    PostCommentView
)


router = DefaultRouter(trailing_slash=False)
router.register(r'posts', PostViewSet)

urlpatterns = [
    path(r'posts/<int:pk>/comments', PostCommentCreateView.as_view()),
    path(r'posts/<int:pk>/comments/<int:id>', PostCommentView.as_view()),
]

urlpatterns += router.urls

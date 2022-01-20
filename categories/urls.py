from django.urls import path
from .views import (
    CategoryView,
    CategoryListCreateView
)


urlpatterns = [
    path(r'bo/categories', CategoryListCreateView.as_view()),
    path(r'bo/categories/<int:pk>', CategoryView.as_view())
]

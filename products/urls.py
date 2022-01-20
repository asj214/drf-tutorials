from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import (
    BrandViewSet,
    ProductViewSet,
    ProductApprovalView
)


router = DefaultRouter(trailing_slash=False)
router.register(r'bo/brands', BrandViewSet)
router.register(r'bo/products', ProductViewSet)

urlpatterns = [
    path(r'bo/products/<int:pk>/approvals', ProductApprovalView.as_view())
]
urlpatterns += router.urls

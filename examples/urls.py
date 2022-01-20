from django.urls import path
from rest_framework.routers import DefaultRouter


router = DefaultRouter(trailing_slash=False)
# router.register(r'artists', ArtistViewSet)
# router.register(r'products', ProductViewSet)

urlpatterns = []
urlpatterns += router.urls

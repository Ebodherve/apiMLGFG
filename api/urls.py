from django.urls import path
from rest_framework.routers import DefaultRouter
from rest_framework.routers import DefaultRouter

from api.views import (UserLoginViewSet, UserViewSet, ProductViewSet, UploadImageViewSet, ProductPOSTViewSet)

router = DefaultRouter()


router.register('register', UserViewSet, basename='register')
router.register('login', UserLoginViewSet, basename='login')
router.register('image', UploadImageViewSet, basename='image')
router.register('product', ProductViewSet, basename='product')


urlpatterns = [
    path("product/<title>/", ProductViewSet.as_view({'get': 'list'}), name="product"),
    # path("image/", UploadImageViewSet.as_view({'post': 'create'}), name="image"),
]


urlpatterns += router.urls

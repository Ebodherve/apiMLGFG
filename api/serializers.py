from rest_framework.serializers import ModelSerializer

from api.models import ProductModel, ImageModel

from django.contrib.auth import get_user_model

User = get_user_model()


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "username", "password", "email")


class UserLoginSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "username", "password")


class ProductSerializer(ModelSerializer):
    class Meta:
        model = ProductModel
        fields = ('id', 'title', 'description')


class ImageSerializer(ModelSerializer):
    class Meta:
        model = ImageModel
        fields = ('id', 'image',)



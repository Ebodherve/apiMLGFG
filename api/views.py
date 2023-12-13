# from django.shortcuts import render
import os
import cv2
from django.contrib.auth import get_user_model
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework.authtoken.models import Token

from rest_framework.viewsets import GenericViewSet
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.mixins import (CreateModelMixin, DestroyModelMixin, ListModelMixin, 
                                   UpdateModelMixin, RetrieveModelMixin)

from api.serializers import UserSerializer, UserLoginSerializer, ProductSerializer, ImageSerializer
from api.models import ProductModel, ImageModel
from api.load_model import ModelYolov




User = get_user_model()
modelY = ModelYolov()
# Create your views here.


def extract_keywords(description):
    c_path = os.getcwd()
    print(c_path)
    fileK = open(c_path + "/api/keys.txt", mode="r")
    keywordS = [w[:-1] for w in fileK.readlines()]

    return list(set(description.split()).intersection(keywordS))


class UserViewSet(CreateModelMixin, GenericViewSet):
    serializer_class = UserSerializer
    permission_classes = (AllowAny,)
    
    def get_queryset(self):
        return User.objects.all()
    
    def create(self, request, *args, **kwargs):
        if User.objects.filter(username=request.POST["username"]).exists():
            return JsonResponse("This user's already exist", safe=False, status=500)
        userC = User.objects.create(username=request.POST["username"], password=request.POST["password"], email=request.POST["email"])
        if userC:
            to = Token.objects.create(user=userC)
            return Response({"Token" : to.key}, status=201)
        return JsonResponse("Something wrong went.", safe=False, status=500) 


class UserLoginViewSet(CreateModelMixin, GenericViewSet):
    serializer_class = UserLoginSerializer
    permission_classes = (AllowAny,)
    
    def get_queryset(self):
        return User.objects.all()
    
    def create(self, request, *args, **kwargs):
        
        jdata = request.data
        if not (jdata.get("username") or jdata.get("password")):
            rep = Response(data='', status=400)
            return rep
        user = User.objects.filter(username=jdata['username'], password=jdata['password'])
        if user.exists():
            user = user.first()
            to, _ = Token.objects.get_or_create(user=user)
            return Response({"Token":to.key}, status=200)
        else:
            rep = Response(data="This user doe's not exist", status=404)
            return rep


class UploadImageViewSet(CreateModelMixin, GenericViewSet):
    serializer_class = ImageSerializer
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)
    
    def get_queryset(self):
        return ImageModel.objects.all()
    
    def create(self, request, *args, **kwargs):

        ResSuper = super().create(request, *args, **kwargs)
        imO = ImageModel.objects.filter(pk=ResSuper.data["id"]).first()
        imName = os.getcwd()+ "/media/" + imO.image.name
        print(imName)
        print(modelY.detection(imName))
        
        return JsonResponse({"keywords" : modelY.detection(imName)}, status=201)


class ProductViewSet(CreateModelMixin, ListModelMixin, GenericViewSet):
    serializer_class = ProductSerializer
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)
    
    def get_queryset(self):
        return ProductModel.objects.all()
    
    def list(self, request, *args, **kwargs):
        prods = ProductModel.objects.filter(title=kwargs["title"])
        if prods.exists():
            p = prods.first()
            return JsonResponse({"description":p.description, "keywords":extract_keywords(p.description)}, status=200)
        return JsonResponse({"description":"", "keywords":[]}, status=404)


class ProductPOSTViewSet(CreateModelMixin, GenericViewSet):
    serializer_class = ProductSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    
    def get_queryset(self):
        return super().get_queryset()
    
    



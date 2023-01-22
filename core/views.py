from django.contrib.auth.models import User
from rest_framework.generics import get_object_or_404

from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from .jwt import get_token_for_user
from .models import UserCompanyExtend, UserInfluExtend, Basket
from .serializers import (UserInfluSerializer, UserCompanySerializer, UserLoginSerializer, UserInfluListSerializer,
                          ContactSerializer, BasketSerializer, UserDasboardSerializer)


class UserCompanyCreateView(APIView):
    model = UserCompanyExtend
    serializer_class = UserCompanySerializer

    def post(self, request):
        sr = self.serializer_class(data=self.request.data)
        if sr.is_valid():
            sr_data = sr.validated_data
            row = self.model(
                fullname=sr_data['fullname'], phone_number=sr_data['phone_number'])
            user = User.objects.create_user(
                username=sr_data['fullname'], password=sr_data['password']
            )
            row.user = user
            row.save()
            token = get_token_for_user(user)
            return Response(data={'token': token}, status=status.HTTP_201_CREATED)
        return Response(data=sr.errors, status=status.HTTP_400_BAD_REQUEST)


class UserInfluCreateView(APIView):
    model = UserInfluExtend
    serializer_class = UserInfluSerializer

    def post(self, request):
        sr = self.serializer_class(data=self.request.data)
        if sr.is_valid():
            sr_data = sr.validated_data
            row = self.model(
                fullname=sr_data['fullname'], phone_number=sr_data['phone_number'], page_id=sr_data['page_id'],
                follower_count=sr_data['follower_count'])
            try:
                user = User.objects.create_user(
                    username=sr_data['fullname'], password=sr_data['password']
                )
            except:
                return Response(data={'errors': 'fullname already exists'}, status=status.HTTP_400_BAD_REQUEST)
            row.user = user
            row.save()
            token = get_token_for_user(user)
            return Response(data={'token': token}, status=status.HTTP_201_CREATED)
        return Response(data=sr.errors, status=status.HTTP_400_BAD_REQUEST)


class UserLoginView(APIView):
    serializer_class = UserLoginSerializer

    def post(self, request):
        sr = self.serializer_class(data=request.data)
        if sr.is_valid(raise_exception=True):
            return Response(data={'token': sr.validated_data['token']}, status=status.HTTP_201_CREATED)


class InfluListView(APIView):
    class_serializer = UserInfluListSerializer

    def get_queryset(self):
        return UserInfluExtend.objects.all()

    def get(self, request):
        sr_data = self.class_serializer(instance=self.get_queryset(), many=True)
        return Response(sr_data.data, status=status.HTTP_200_OK)


class ContactView(APIView):
    class_serializer = ContactSerializer

    def post(self, request):
        sr_data = self.class_serializer(data=request.data)
        if sr_data.is_valid(raise_exception=True):
            sr_data.save()
            return Response(data=sr_data.data, status=status.HTTP_201_CREATED)


class PaymentDetailView(APIView):
    class_serializer = UserInfluListSerializer

    def get(self, request, influ_id):
        influ = get_object_or_404(UserInfluExtend, id=influ_id)
        sr_data = self.class_serializer(instance=influ)
        return Response(sr_data.data, status=status.HTTP_200_OK)


class PaymentBuyView(IsAuthenticated, APIView):
    class_serializer = BasketSerializer

    def get(self, request, influ_id):
        influ = get_object_or_404(UserInfluExtend, id=influ_id)
        basket = Basket(influ=influ, price='22000', is_paid=True)
        user_company = UserCompanyExtend.objects.filter(user=request.user.id)
        if user_company.exists():
            basket.company = user_company.first()
        basket.save()
        sr = self.class_serializer(instance=basket)
        return Response(data=sr.data, status=status.HTTP_200_OK)


class DashboardView(IsAuthenticated, APIView):
    class_serializer = UserDasboardSerializer

    def get(self, request):
        company = UserCompanyExtend.objects.filter(user=request.user.id)
        if company.exists():
            sr = self.class_serializer(instance=company.first())
            return Response(data=sr.data, status=status.HTTP_200_OK)
        influ = UserInfluExtend.objects.filter(user=request.user.id)
        if influ:
            sr = self.class_serializer(instance=influ.first())
            return Response(data=sr.data, status=status.HTTP_200_OK)



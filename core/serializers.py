from django.contrib.auth import authenticate
from django.db.models import Q

from rest_framework import serializers
from rest_framework.response import Response

from .models import UserCompanyExtend, UserInfluExtend, Contact, Basket
from .jwt import get_token_for_user


class UserCompanySerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=18)

    class Meta:
        model = UserCompanyExtend
        fields = ('fullname', 'phone_number', 'password')
        extra_kwargs = {"password": {"write_only": True}}


class UserInfluSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=18)

    class Meta:
        model = UserInfluExtend
        fields = ('fullname', 'phone_number', 'page_id', 'follower_count', 'password')
        extra_kwargs = {"password": {"write_only": True}}


class UserLoginSerializer(serializers.Serializer):
    fullname = serializers.CharField(max_length=34)
    password = serializers.CharField(max_length=64)

    def validate(self, attrs):
        user = authenticate(username=attrs['fullname'], password=attrs['password'])
        if not user:
            raise serializers.ValidationError('invalid data')
        token = get_token_for_user(user)
        attrs['token'] = token
        return attrs


class UserInfluListSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserInfluExtend
        fields = ('id', 'fullname', 'phone_number', 'page_id', 'follower_count', 'user')


class UserCompanyListSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserCompanyExtend
        fields = ('fullname', 'phone_number', 'password')


class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = '__all__'


class BasketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Basket
        fields = '__all__'


class BasketListSerializer(serializers.ModelSerializer):
    company = serializers.SerializerMethodField(method_name='get_company')
    influ = serializers.SerializerMethodField(method_name='get_influ')

    class Meta:
        model = Basket
        fields = '__all__'

    def get_company(self, obj):
        if obj.company:
            company = UserCompanyExtend.objects.filter(id=obj.company)
            return UserCompanyListSerializer(instance=company.first()).data
        return None

    def get_influ(self, obj):
        if obj.influ:
            influ = UserInfluExtend.objects.filter(id=obj.influ_id)
            return UserInfluListSerializer(instance=influ.first()).data


class UserDasboardSerializer(serializers.Serializer):
    fullname = serializers.CharField(max_length=34)
    phone_number = serializers.CharField(max_length=18)
    page_id = serializers.CharField(max_length=34, required=False)
    follower_count = serializers.IntegerField(required=False)

    ads = serializers.SerializerMethodField('get_orders', read_only=True)

    def get_orders(self, obj):
        baskets = Basket.objects.filter(Q(company__fullname=obj.fullname) | Q(influ__fullname=obj.fullname))
        return BasketListSerializer(instance=baskets, many=True).data

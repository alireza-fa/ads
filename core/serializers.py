from django.contrib.auth import authenticate
from django.db.models import Q
from django.contrib.auth.models import User

from rest_framework import serializers

from .models import UserCompanyExtend, UserInfluExtend, Contact, Basket, ContactUs
from .jwt import get_token_for_user


class UserCompanySerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=18)

    class Meta:
        model = UserCompanyExtend
        fields = ('fullname', 'phone_number', 'password')
        extra_kwargs = {"password": {"write_only": True}}

    def validate_fullname(self, value):
        user = User.objects.filter(username=value)
        if user.exists():
            raise serializers.ValidationError('fullname already exists')
        return value


class UserInfluSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=18)

    class Meta:
        model = UserInfluExtend
        fields = ('fullname', 'phone_number', 'page_id', 'follower_count', 'password', 'image', 'category', 'price')
        extra_kwargs = {"password": {"write_only": True}}

    def validate_fullname(self, value):
        user = User.objects.filter(username=value)
        if user.exists():
            raise serializers.ValidationError('fullname already exists')
        return value


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
        fields = ('id', 'fullname', 'phone_number', 'page_id', 'follower_count', 'user', 'image', 'category', 'price')


class UserCompanyListSerializer(serializers.Serializer):
    fullname = serializers.SerializerMethodField('get_fullname', read_only=True)
    phone_number = serializers.SerializerMethodField('get_phone_number', read_only=True)

    def get_fullname(self, obj):
        return obj.username

    def get_phone_number(self, obj):
        try:
            return obj.company.phone_number
        except:
            return obj.influ.phone_number


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
            company = User.objects.filter(username=obj.company.username)
            return UserCompanyListSerializer(instance=company.first()).data
        return None

    def get_influ(self, obj):
        if obj.influ:
            influ = UserInfluExtend.objects.filter(fullname=obj.influ.username)
            return UserInfluListSerializer(instance=influ.first()).data


class UserDasboardSerializer(serializers.Serializer):
    fullname = serializers.CharField(max_length=34)
    phone_number = serializers.CharField(max_length=18)
    page_id = serializers.CharField(max_length=34, required=False)
    follower_count = serializers.IntegerField(required=False)
    price = serializers.IntegerField(required=False)

    ads = serializers.SerializerMethodField('get_orders', read_only=True)

    def get_orders(self, obj):
        baskets = Basket.objects.filter(Q(company__username=obj.fullname) | Q(influ__username=obj.fullname))
        return BasketListSerializer(instance=baskets, many=True).data


class ContactUsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactUs
        fields = '__all__'

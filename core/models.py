from django.db import models
from django.contrib.auth.models import User


class UserCompanyExtend(models.Model):
    fullname = models.CharField(max_length=34, unique=True)
    phone_number = models.CharField(max_length=18)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='company')

    def __str__(self):
        return self.fullname


class UserInfluExtend(models.Model):
    fullname = models.CharField(max_length=34, unique=True)
    image = models.ImageField()
    phone_number = models.CharField(max_length=18)
    page_id = models.CharField(max_length=64)
    category = models.CharField(max_length=34)
    price = models.PositiveIntegerField()
    follower_count = models.PositiveIntegerField()
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='influ', unique=True)

    def __str__(self):
        return self.fullname


class Contact(models.Model):
    name = models.CharField(max_length=34)
    phone_number = models.CharField(max_length=18)
    subject = models.CharField(max_length=76)
    message = models.TextField()

    def __str__(self):
        return self.name


class Basket(models.Model):
    company = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='influs', null=True, blank=True)
    influ = models.ForeignKey(User, on_delete=models.CASCADE, related_name='companies')
    price = models.PositiveIntegerField()
    is_paid = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.price}'


class ContactUs(models.Model):
    message = models.TextField()

    def __str__(self):
        return f'contact us {self.id}'

    class Meta:
        verbose_name = 'Complaint'
        verbose_name_plural = 'complaints'

# Generated by Django 4.1.5 on 2023-01-22 00:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_alter_userinfluextend_fullname'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usercompanyextend',
            name='phone_number',
            field=models.CharField(max_length=18),
        ),
    ]
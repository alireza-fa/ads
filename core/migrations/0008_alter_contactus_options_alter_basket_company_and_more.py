# Generated by Django 4.1.5 on 2023-01-23 12:32

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('core', '0007_contactus_userinfluextend_category_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='contactus',
            options={'verbose_name': 'Complaint', 'verbose_name_plural': 'complaints'},
        ),
        migrations.AlterField(
            model_name='basket',
            name='company',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='influs', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='basket',
            name='influ',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='companies', to=settings.AUTH_USER_MODEL),
        ),
    ]

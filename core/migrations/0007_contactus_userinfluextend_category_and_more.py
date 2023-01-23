# Generated by Django 4.1.5 on 2023-01-23 11:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_alter_basket_company'),
    ]

    operations = [
        migrations.CreateModel(
            name='ContactUs',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.TextField()),
            ],
        ),
        migrations.AddField(
            model_name='userinfluextend',
            name='category',
            field=models.CharField(default='good', max_length=34),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='userinfluextend',
            name='image',
            field=models.ImageField(default='image.png', upload_to=''),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='userinfluextend',
            name='price',
            field=models.PositiveIntegerField(default=22000),
            preserve_default=False,
        ),
    ]
# Generated by Django 3.2.8 on 2021-10-30 00:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_user_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='image',
            field=models.ImageField(blank=True, default='default.png', upload_to='profile_pics'),
        ),
    ]
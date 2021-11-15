# Generated by Django 3.2.8 on 2021-11-15 11:24

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0010_auto_20211115_2041'),
        ('avatar', '0004_alter_avatar_id'),
        ('admin', '0003_logentry_add_action_flag_choices'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('account', '0003_auto_20211115_2123'),
        ('socialaccount', '0004_auto_20211115_2123'),
        ('groups', '0001_initial'),
        ('accounts', '0006_userprofile_followers'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='followers',
            field=models.ManyToManyField(blank=True, related_name='followers', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, related_name='profile', serialize=False, to=settings.AUTH_USER_MODEL, verbose_name='user'),
        ),
        migrations.DeleteModel(
            name='User',
        ),
    ]

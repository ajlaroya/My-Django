# Generated by Django 3.2.8 on 2021-12-15 09:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0019_alter_comment_post'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='comment',
            options={'ordering': ['timestamp']},
        ),
    ]
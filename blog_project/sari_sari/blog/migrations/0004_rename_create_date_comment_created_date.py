# Generated by Django 3.2.7 on 2021-09-26 07:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_rename_create_date_post_created_date'),
    ]

    operations = [
        migrations.RenameField(
            model_name='comment',
            old_name='create_date',
            new_name='created_date',
        ),
    ]

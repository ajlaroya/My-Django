# Generated by Django 3.2.8 on 2021-11-22 10:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0010_notification_thread'),
    ]

    operations = [
        migrations.AlterField(
            model_name='messagemodel',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='uploads/message_photos'),
        ),
    ]

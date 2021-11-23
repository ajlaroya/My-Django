# Generated by Django 3.2.8 on 2021-11-22 10:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0017_alter_post_image'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
            ],
        ),
        migrations.AddField(
            model_name='comment',
            name='tags',
            field=models.ManyToManyField(blank=True, to='posts.Tag'),
        ),
        migrations.AddField(
            model_name='post',
            name='tags',
            field=models.ManyToManyField(blank=True, to='posts.Tag'),
        ),
    ]

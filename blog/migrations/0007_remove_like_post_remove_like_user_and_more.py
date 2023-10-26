# Generated by Django 4.2.4 on 2023-10-19 17:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0006_post_dislikes_like_dislike'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='like',
            name='post',
        ),
        migrations.RemoveField(
            model_name='like',
            name='user',
        ),
        migrations.AlterField(
            model_name='post',
            name='categories',
            field=models.ManyToManyField(null=True, related_name='posts', to='blog.category'),
        ),
        migrations.DeleteModel(
            name='Dislike',
        ),
        migrations.DeleteModel(
            name='Like',
        ),
    ]

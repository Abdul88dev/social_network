# Generated by Django 4.1.4 on 2022-12-16 19:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customers', '0002_rename_post_comment_post_remove_post_content_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='main_img',
            field=models.ImageField(blank=True, null=True, upload_to='images/'),
        ),
    ]

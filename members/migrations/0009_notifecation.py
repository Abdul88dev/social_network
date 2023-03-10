# Generated by Django 4.1.4 on 2023-01-03 16:06

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('customers', '0012_alter_post_title'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('members', '0008_remove_profile_follownig_agent'),
    ]

    operations = [
        migrations.CreateModel(
            name='Notifecation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(choices=[('C', 'Comment'), ('F', 'Follow'), ('L', 'Like')], max_length=1)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('seen', models.BooleanField(default=False)),
                ('notified', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='notification_reciever', to=settings.AUTH_USER_MODEL)),
                ('notifier', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='notification_sender', to=settings.AUTH_USER_MODEL)),
                ('post', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='post_notification', to='customers.post')),
            ],
        ),
    ]

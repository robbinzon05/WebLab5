# Generated by Django 5.1.3 on 2024-12-24 09:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_remove_profile_avatar_profile_avatar_id'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Profile',
        ),
    ]

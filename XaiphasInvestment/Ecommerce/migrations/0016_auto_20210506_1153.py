# Generated by Django 3.1.7 on 2021-05-06 08:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Ecommerce', '0015_wallet_user_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='wallet',
            name='created_at',
        ),
        migrations.RemoveField(
            model_name='wallet',
            name='updated_at',
        ),
        migrations.RemoveField(
            model_name='wallet',
            name='user_id',
        ),
        migrations.AddField(
            model_name='wallet',
            name='user_name',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]

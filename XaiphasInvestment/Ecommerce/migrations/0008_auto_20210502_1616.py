# Generated by Django 3.1.7 on 2021-05-02 13:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Ecommerce', '0007_auto_20210502_0653'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='category',
            field=models.CharField(choices=[('Men', 'Men'), ('Women', 'Women'), ('Children', 'Children')], max_length=200),
        ),
    ]

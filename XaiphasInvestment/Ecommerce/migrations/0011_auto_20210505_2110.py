# Generated by Django 3.1.7 on 2021-05-05 18:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Ecommerce', '0010_wallet'),
    ]

    operations = [
        migrations.RenameField(
            model_name='mpesapayment',
            old_name='reference',
            new_name='transaction_type',
        ),
        migrations.RemoveField(
            model_name='mpesapayment',
            name='organization_balance',
        ),
        migrations.RemoveField(
            model_name='mpesapayment',
            name='type',
        ),
        migrations.AddField(
            model_name='mpesapayment',
            name='transaction_id',
            field=models.CharField(default='12332', max_length=50),
            preserve_default=False,
        ),
    ]

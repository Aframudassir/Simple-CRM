# Generated by Django 5.0.1 on 2024-09-17 19:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_usersubscribermapping_paid'),
    ]

    operations = [
        migrations.AddField(
            model_name='subscriptionplan',
            name='category',
            field=models.CharField(choices=[('CRYPTO', 'CRYPTO'), ('STOCKS', 'STOCKS'), ('Commodity', 'Commodity')], default='STOCKS', max_length=100),
        ),
    ]

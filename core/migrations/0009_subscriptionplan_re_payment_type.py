# Generated by Django 5.0.1 on 2024-10-13 09:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0008_remove_investmentsmapping_investment_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='subscriptionplan',
            name='re_payment_type',
            field=models.CharField(choices=[('MONTHLY', 'MONTHLY'), ('END_OF_TERM', 'END_OF_TERM')], default='MONTHLY', max_length=100),
        ),
    ]
# Generated by Django 3.1.7 on 2021-05-25 23:07

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Bag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('asset', models.CharField(choices=[('BTC', 'BTC'), ('ETH', 'ETH'), ('LTC', 'LTC'), ('AAVE', 'AAVE'), ('XTZ', 'XTZ'), ('GRT', 'GRT')], default='BTC', max_length=254, verbose_name='asset')),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(default=django.utils.timezone.now, verbose_name='order date')),
                ('amount', models.FloatField(default=0, verbose_name='amount')),
                ('price', models.FloatField(default=0, verbose_name='buy price')),
                ('bag', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='orders', to='wallets.bag')),
            ],
        ),
    ]

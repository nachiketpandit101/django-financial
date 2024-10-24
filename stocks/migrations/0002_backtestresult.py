# Generated by Django 5.1.2 on 2024-10-25 18:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stocks', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='BacktestResult',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('initial_investment', models.DecimalField(decimal_places=2, max_digits=15)),
                ('final_portfolio_value', models.DecimalField(decimal_places=2, max_digits=15)),
                ('total_return', models.DecimalField(decimal_places=2, max_digits=15)),
                ('max_drawdown', models.DecimalField(decimal_places=2, max_digits=15)),
                ('trade_count', models.IntegerField()),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]

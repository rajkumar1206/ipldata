# Generated by Django 3.1.3 on 2020-11-27 08:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('matches', '0004_appuser_username'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appuser',
            name='key',
            field=models.CharField(max_length=50, primary_key=True, serialize=False),
        ),
    ]

# Generated by Django 5.1.1 on 2024-11-27 04:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userdepositaccount',
            name='account_no',
            field=models.IntegerField(editable=False, unique=True),
        ),
    ]

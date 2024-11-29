# Generated by Django 5.1.1 on 2024-11-27 18:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Book', '0004_bookmodel_is_borrowed'),
        ('reviews', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='bookmodel',
            name='reviews',
            field=models.ManyToManyField(blank=True, related_name='book_reviews', to='reviews.review'),
        ),
    ]
# Generated by Django 3.1.1 on 2020-10-21 15:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0003_auto_20201020_1511'),
    ]

    operations = [
        migrations.AddField(
            model_name='watchlist',
            name='listing_id',
            field=models.IntegerField(default=4),
            preserve_default=False,
        ),
    ]

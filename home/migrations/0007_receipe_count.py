# Generated by Django 4.2.3 on 2023-08-08 19:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0006_receipe_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='receipe',
            name='count',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
    ]

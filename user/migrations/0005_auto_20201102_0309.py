# Generated by Django 3.1 on 2020-11-02 03:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0004_owner_owner_email'),
    ]

    operations = [
        migrations.AlterField(
            model_name='owner',
            name='owner_id',
            field=models.CharField(default='0000000', max_length=10),
        ),
        migrations.AlterField(
            model_name='pet',
            name='pet_id',
            field=models.CharField(default='0000000', max_length=10),
        ),
    ]

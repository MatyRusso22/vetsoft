# Generated by Django 5.0.6 on 2024-05-19 22:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0008_pet_weigth_alter_product_id'),
    ]

    operations = [
        migrations.RenameField(
            model_name='pet',
            old_name='weigth',
            new_name='weight',
        ),
    ]

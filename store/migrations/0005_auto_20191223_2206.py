# Generated by Django 2.2.3 on 2019-12-23 16:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0004_orders'),
    ]

    operations = [
        migrations.RenameField(
            model_name='orders',
            old_name='add',
            new_name='address',
        ),
        migrations.RenameField(
            model_name='orders',
            old_name='zipcode',
            new_name='zip_code',
        ),
    ]
